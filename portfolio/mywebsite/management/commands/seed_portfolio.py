import json
from pathlib import Path

from django.conf import settings
from django.core.files import File
from django.core.management.base import BaseCommand, CommandError

from mywebsite.models import ImageGallary, Project


class Command(BaseCommand):
    help = "Seed the existing portfolio projects and gallery images."

    def handle(self, *args, **options):
        data_file = Path(settings.BASE_DIR) / "seed_data" / "portfolio.json"
        media_root = Path(settings.BASE_DIR) / "seed_media"

        if not data_file.exists():
            raise CommandError(f"Seed data file not found: {data_file}")

        data = json.loads(data_file.read_text(encoding="utf-8"))
        project_map = {}

        for item in data.get("projects", []):
            project, created = Project.objects.get_or_create(
                title=item["title"],
                defaults={
                    "description": item["description"],
                    "link": item["link"],
                    "tech_stack": item.get("tech_stack") or "",
                    "github_link": item.get("github_link") or None,
                },
            )

            if not project.image:
                self._attach_image(project, "image", item["image"], media_root)

            project_map[item["id"]] = project
            self.stdout.write(
                f'{"Created" if created else "Found"} project: {project.title}'
            )

        for item in data.get("galleries", []):
            project = project_map.get(item["project_id"])
            if project is None:
                continue

            filename = Path(item["image"]).name
            already_exists = any(
                Path(g.image.name).name == filename
                for g in project.images.all()
                if g.image
            )

            if not already_exists:
                gallery = ImageGallary(project=project)
                self._attach_image(gallery, "image", item["image"], media_root)

        self.stdout.write(self.style.SUCCESS("Portfolio seed completed."))

    def _attach_image(self, instance, field_name, relative_name, media_root):
        source = media_root / relative_name
        if not source.exists():
            raise CommandError(f"Seed image not found: {source}")

        with source.open("rb") as image_file:
            getattr(instance, field_name).save(
                source.name,
                File(image_file),
                save=True,
            )
