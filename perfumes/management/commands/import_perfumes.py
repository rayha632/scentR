import json

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import transaction

from perfumes.models import Perfume


class Command(BaseCommand):
    help = "Import Scento perfumes from JSONL into PostgreSQL"

    def handle(self, *args, **options):
        file_path = settings.BASE_DIR / "data" / "perfumes.jsonl"

        created_count = 0
        updated_count = 0

        # Open the file and start a database transaction
        with transaction.atomic(), open(file_path, encoding="utf-8") as file:
            for line in file:
                record = json.loads(line)

                # Update an existing perfume or create a new one
                _, created = Perfume.objects.update_or_create(
                    id=record["id"],
                    defaults={
                        "name": record["name"],
                        "house": record["house"],
                        "family": record.get("family") or "",
                        "secondary_family": record.get("secondary_family") or "",
                        "notes": record.get("notes") or [],
                        "top_notes": record.get("top_notes") or [],
                        "heart_notes": record.get("heart_notes") or [],
                        "base_notes": record.get("base_notes") or [],
                        "character": record.get("character") or [],
                        "seasons": record.get("seasons") or [],
                        "times_of_day": record.get("times_of_day") or [],
                        "description": record.get("description") or "",
                    },
                )

                if created:
                    created_count += 1
                else:
                    updated_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Imported {created_count} new perfumes, "
                f"updated {updated_count} existing perfumes."
            )
        )
