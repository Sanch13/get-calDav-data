"""Мониторинг доступности Bitrix API с уведомлениями в Telegram.

Состояние ведётся по каждой комнате отдельно, сообщения собираются в одно:

    up   --(сбой дольше BITRIX_FAIL_GRACE_SECONDS)-->  down  -> алерт + эскалация
    down --(успех дольше BITRIX_RECOVERY_CONFIRM_SECONDS)-->  up  -> одно сообщение о восстановлении

Короткие сбои (меньше BITRIX_FAIL_GRACE_SECONDS) не порождают ни алерта,
ни сообщения о восстановлении — остаётся только запись в логе.
Сообщение о восстановлении уходит один раз на инцидент и только если
по пострадавшим комнатам действительно уходил алерт.
"""

import datetime
import logging

from django.conf import settings
from django.core.cache import cache
from django.utils import timezone

from rooms.services.telegram import send_telegram_message

logger = logging.getLogger(__name__)

STATE_DOWN = "down"
STATE_UP = "up"

KEY_PREFIX = "bitrix"

STATE_TTL = 6 * 60 * 60       # время жизни состояния инцидента
FAIL_STREAK_TTL = 10 * 60     # счётчик неудачных запросов подряд
QUIET_TTL = 60 * 60           # подтверждение восстановления
RECOVERED_TTL = 24 * 60 * 60  # накопленные восстановления в рамках инцидента
COOLDOWN_TTL = 10 * 60        # антиспам между сообщениями


def _key(name: str, slug: str = "") -> str:
    return f"{KEY_PREFIX}:{name}:{slug}" if slug else f"{KEY_PREFIX}:{name}"


def _read_dt(name: str, slug: str = "") -> datetime.datetime | None:
    raw = cache.get(_key(name, slug))
    return datetime.datetime.fromisoformat(raw) if raw else None


def _minutes(delta: datetime.timedelta) -> int:
    return int(delta.total_seconds() // 60)


def _room_name(slug: str) -> str:
    return settings.MEETING_ROOMS.get(slug, {}).get("name", slug)


def _rooms_summary(rooms: dict) -> str:
    now = timezone.now()
    return ", ".join(
        f"«{_room_name(slug)}» (простой {_minutes(now - down_since)} мин)"
        for slug, down_since in sorted(rooms.items(), key=lambda item: item[1])
    )


def _down_rooms() -> dict:
    rooms = {}
    for slug in settings.MEETING_ROOMS:
        if cache.get(_key("state", slug)) == STATE_DOWN:
            rooms[slug] = _read_dt("down_since", slug) or timezone.now()
    return rooms


def record_failure(room_slug: str) -> None:
    """Регистрирует неудачный запрос к Bitrix и при необходимости шлёт алерт."""
    now = timezone.now()

    streak = cache.get(_key("fail", room_slug)) or {}
    first_fail = datetime.datetime.fromisoformat(streak["first_fail"]) if streak.get("first_fail") else now
    fails_in_row = streak.get("count", 0) + 1
    cache.set(
        _key("fail", room_slug),
        {"first_fail": first_fail.isoformat(), "count": fails_in_row},
        timeout=FAIL_STREAK_TTL,
    )

    if cache.get(_key("state", room_slug)) == STATE_DOWN:
        _try_escalate(room_slug, now)
        return

    age = (now - first_fail).total_seconds()
    if age < settings.BITRIX_FAIL_GRACE_SECONDS:
        logger.info(
            "Сбой Bitrix на комнате «%s»: ошибок подряд %d, прошло %d c — в пределах допуска, "
            "уведомление не отправляем",
            _room_name(room_slug), fails_in_row, age,
        )
        return

    cache.set(_key("state", room_slug), STATE_DOWN, timeout=STATE_TTL)
    cache.set(_key("down_since", room_slug), first_fail.isoformat(), timeout=STATE_TTL)
    cache.set(_key("alerts", room_slug), 0, timeout=STATE_TTL)
    logger.warning(
        "Bitrix не отвечает на комнате «%s» дольше %d c — считаем аварией",
        _room_name(room_slug), age,
    )
    _try_escalate(room_slug, now)


def record_success(room_slug: str) -> None:
    """Регистрирует успешный ответ Bitrix и при необходимости шлёт восстановление."""
    if not cache.get(_key("tracking")):
        # Активных инцидентов нет — держим только чистый счётчик сбоев,
        # чтобы короткий сбой не «приклеивался» к следующему.
        cache.delete(_key("fail", room_slug))
        return

    if cache.get(_key("state", room_slug)) != STATE_DOWN:
        cache.delete(_key("fail", room_slug))
        cache.delete(_key("quiet", room_slug))
        return

    quiet_since = _read_dt("quiet", room_slug)
    if quiet_since is None:
        cache.set(_key("quiet", room_slug), timezone.now().isoformat(), timeout=QUIET_TTL)
        cache.delete(_key("fail", room_slug))
        return

    quiet_for = (timezone.now() - quiet_since).total_seconds()
    if quiet_for < settings.BITRIX_RECOVERY_CONFIRM_SECONDS:
        logger.info(
            "Bitrix на комнате «%s» ответил, ждём подтверждения восстановления (%d c из %d)",
            _room_name(room_slug), quiet_for, settings.BITRIX_RECOVERY_CONFIRM_SECONDS,
        )
        return

    _mark_recovered(room_slug)


def _try_escalate(room_slug: str, now: datetime.datetime) -> None:
    down_since = _read_dt("down_since", room_slug) or now
    sent = cache.get(_key("alerts", room_slug), 0)
    schedule = settings.BITRIX_ESCALATION_SECONDS

    # Наблюдение нужно только пока идёт реальный инцидент.
    cache.set(_key("tracking"), 1, timeout=STATE_TTL)

    while sent < len(schedule) and (now - down_since).total_seconds() >= schedule[sent]:
        if not _send_alert(room_slug, sent + 1, now):
            # Сообщение подавлено антиспамом или не доставлено — вернёмся к нему
            # на следующем неудачном запросе, не сдвигая счётчик.
            return
        sent += 1
        break  # за один запрос — не больше одного сообщения


def _send_alert(room_slug: str, alert_no: int, now: datetime.datetime) -> bool:
    last_message = _read_dt("cooldown")
    if last_message and (now - last_message).total_seconds() < settings.BITRIX_ALERT_COOLDOWN_SECONDS:
        logger.info("Алерт Bitrix (%d) подавлен антиспамом", alert_no)
        return False

    down = _down_rooms()
    total = len(settings.BITRIX_ESCALATION_SECONDS)
    header = "🔴 Bitrix не отвечает" if alert_no == 1 else f"🔴 Bitrix всё ещё недоступен ({alert_no}/{total})"
    if not send_telegram_message(f"{header} — {_rooms_summary(down)}"):
        return False

    cache.set(_key("alerts", room_slug), alert_no, timeout=STATE_TTL)
    cache.set(_key("cooldown"), now.isoformat(), timeout=COOLDOWN_TTL)
    return True


def _mark_recovered(room_slug: str) -> None:
    now = timezone.now()
    down_since = _read_dt("down_since", room_slug) or now
    alerts = cache.get(_key("alerts", room_slug), 0)

    for name in ("fail", "quiet", "state", "down_since", "alerts"):
        cache.delete(_key(name, room_slug))

    recovered = cache.get(_key("recovered")) or {}
    recovered[room_slug] = {"down_since": down_since.isoformat(), "alerts": alerts}

    still_down = _down_rooms()
    if still_down:
        # Инцидент ещё не закончился: копим восстановления и ждём последнюю комнату,
        # чтобы отправить одно сообщение, а не по одному на каждую.
        cache.set(_key("recovered"), recovered, timeout=RECOVERED_TTL)
        logger.info(
            "Bitrix на комнате «%s» восстановился, ждём остальные: %s",
            _room_name(room_slug), ", ".join(_room_name(slug) for slug in still_down),
        )
        return

    cache.set(_key("cooldown"), now.isoformat(), timeout=COOLDOWN_TTL)
    cache.delete(_key("tracking"))
    cache.delete(_key("recovered"))

    warned = {
        slug: datetime.datetime.fromisoformat(data["down_since"])
        for slug, data in recovered.items()
        if data.get("alerts")
    }
    if not warned:
        logger.info("Bitrix восстановился, но алерты не отправлялись — уведомление не нужно")
        return

    text = (
        f"✅ Bitrix снова отвечает — {_rooms_summary(warned)}\n"
        f"Затронуто комнат: {len(warned)} из {len(settings.MEETING_ROOMS)}"
    )
    send_telegram_message(text)


def snapshot() -> dict:
    """Текущее состояние монитора — для management-команды bitrix_status."""
    rooms = {}
    for slug in settings.MEETING_ROOMS:
        streak = cache.get(_key("fail", slug)) or {}
        rooms[slug] = {
            "state": STATE_DOWN if cache.get(_key("state", slug)) == STATE_DOWN else STATE_UP,
            "down_since": _read_dt("down_since", slug),
            "alerts": cache.get(_key("alerts", slug), 0),
            "quiet_since": _read_dt("quiet", slug),
            "fails_in_row": streak.get("count", 0),
        }

    return {
        "tracking": bool(cache.get(_key("tracking"))),
        "cooldown": _read_dt("cooldown"),
        "recovered": cache.get(_key("recovered")) or {},
        "escalation": settings.BITRIX_ESCALATION_SECONDS,
        "fail_grace": settings.BITRIX_FAIL_GRACE_SECONDS,
        "recovery_confirm": settings.BITRIX_RECOVERY_CONFIRM_SECONDS,
        "rooms": rooms,
    }


def reset() -> None:
    """Сбрасывает всё состояние монитора — для management-команды bitrix_status --reset."""
    names = ("tracking", "cooldown", "recovered")
    per_room = ("fail", "quiet", "state", "down_since", "alerts")
    for name in names:
        cache.delete(_key(name))
    for slug in settings.MEETING_ROOMS:
        for name in per_room:
            cache.delete(_key(name, slug))