from django.core.management.base import BaseCommand
from django.db.models import Count, Min

from apps.events.models import Event


class Command(BaseCommand):
    help = "Elimina eventos duplicados por 'code', conservando solo el primero (por id)"

    def handle(self, *args, **options):
        duplicates = (
            Event.objects
            .values('code')
            .annotate(count=Count('id'))
            .filter(count__gt=1)
            .exclude(code__isnull=True)
        )

        total_deleted = 0

        for entry in duplicates:
            code = entry['code']
            first_event_id = (
                Event.objects
                .filter(code=code)
                .order_by('id')
                .values_list('id', flat=True)
                .first()
            )

            deleted, _ = (
                Event.objects
                .filter(code=code)
                .exclude(id=first_event_id)
                .delete()
            )
            total_deleted += deleted

            self.stdout.write(f"Code '{code}': {deleted} duplicado(s) eliminado(s)")

        self.stdout.write(self.style.SUCCESS(f"Total de eventos eliminados: {total_deleted}"))
