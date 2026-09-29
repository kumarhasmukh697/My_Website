import io
import os
import posixpath
import uuid

import cloudinary
import requests
from django.core.files.base import ContentFile
from django.core.files.storage import Storage
from django.utils.deconstruct import deconstructible


@deconstructible
class CloudinaryMediaStorage(Storage):
    """Django storage backend for image uploads using Cloudinary."""

    def _save(self, name, content):
        name = name.replace("\\", "/").lstrip("/")
        directory, filename = posixpath.split(name)
        stem, extension = os.path.splitext(filename)
        unique_stem = f"{stem}_{uuid.uuid4().hex[:12]}"
        public_id = posixpath.join(directory, unique_stem) if directory else unique_stem

        result = cloudinary.uploader.upload(
            content,
            public_id=public_id,
            resource_type="image",
            overwrite=False,
            use_filename=False,
            unique_filename=False,
            secure=True,
        )

        cloudinary_format = result.get("format") or extension.lstrip(".")
        return f"{public_id}.{cloudinary_format}" if cloudinary_format else public_id

    def exists(self, name):
        # Every upload receives a UUID suffix, so remote collision checks are unnecessary.
        return False

    def url(self, name):
        public_id, extension = os.path.splitext(name)
        options = {"secure": True, "resource_type": "image"}
        if extension:
            options["format"] = extension.lstrip(".")
        url, _ = cloudinary.utils.cloudinary_url(public_id, **options)
        return url

    def delete(self, name):
        public_id = os.path.splitext(name)[0]
        try:
            cloudinary.uploader.destroy(
                public_id,
                resource_type="image",
                invalidate=True,
            )
        except Exception:
            pass

    def size(self, name):
        public_id = os.path.splitext(name)[0]
        result = cloudinary.api.resource(public_id, resource_type="image")
        return int(result.get("bytes", 0))

    def open(self, name, mode="rb"):
        if "w" in mode:
            raise ValueError("CloudinaryMediaStorage does not support local write mode.")
        response = requests.get(self.url(name), timeout=30)
        response.raise_for_status()
        return ContentFile(response.content, name=os.path.basename(name))

    def path(self, name):
        raise NotImplementedError("Cloudinary files do not have a local filesystem path.")
