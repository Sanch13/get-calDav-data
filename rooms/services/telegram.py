import requests

from django.conf import settings

from logs.logging_config import logger


def send_telegram_message(text: str) -> bool:
    """Отправляет сообщение в Telegram-чат.

    Возвращает True только если сообщение действительно доставлено —
    вызывающий код использует это, чтобы не считать недоставленное
    уведомление отправленным и повторить попытку позже.
    """
    url = f"https://api.telegram.org/bot{settings.TG_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": settings.TG_CHAT_ID,
        "message_thread_id": settings.TG_TOPIC_ID,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": True,
    }

    try:
        response = requests.post(url, json=payload, timeout=5)
        response.raise_for_status()
        logger.info("Уведомление в Telegram успешно отправлено!")
        return True
    except Exception:
        logger.exception("Не удалось отправить уведомление в Telegram")
        return False