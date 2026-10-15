from django.core.management.base import BaseCommand

from rooms.services import bitrix_monitor


class Command(BaseCommand):
    help = "Показывает состояние мониторинга Bitrix API (--reset — сбросить состояние)"

    def add_arguments(self, parser):
        parser.add_argument(
            "--reset",
            action="store_true",
            help="Очистить всё состояние монитора (аварию, счётчики, антиспам)",
        )

    def handle(self, *args, **options):
        if options["reset"]:
            bitrix_monitor.reset()
            self.stdout.write(self.style.WARNING("Состояние монитора Bitrix сброшено."))
            return

        snapshot = bitrix_monitor.snapshot()

        self.stdout.write(
            f"Отслеживание инцидента: {'да' if snapshot['tracking'] else 'нет'}\n"
            f"Порог простоя: {snapshot['fail_grace']} c, "
            f"подтверждение восстановления: {snapshot['recovery_confirm']} c, "
            f"эскалация: {snapshot['escalation']} c\n"
            f"Антиспам до: {snapshot['cooldown'] or '—'}\n"
        )

        for slug, room in snapshot["rooms"].items():
            state = self.style.SUCCESS("up") if room["state"] == "up" else self.style.ERROR("down")
            details = f"ошибок подряд: {room['fails_in_row']}"
            if room["state"] == "down":
                details += (
                    f", простой с {room['down_since']:%Y-%m-%d %H:%M}, "
                    f"алертов: {room['alerts']}"
                )
            self.stdout.write(f"  {state:<10} {slug:<10} {details}")