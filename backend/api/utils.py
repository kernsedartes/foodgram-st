import base64
import uuid
import six
import filetype
from rest_framework import serializers
from django.core.files.base import ContentFile


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith("data:image"):
            format, imgstr = data.split(";base64,")
            ext = format.split("/")[-1]
            data = ContentFile(base64.b64decode(imgstr), name=f"image.{ext}")
        return super().to_internal_value(data)

    def to_representation(self, value):
        if not value:
            return None
        try:
            with value.open("rb") as f:
                base64_data = base64.b64encode(f.read()).decode("utf-8")
                return f"data:image/{value.name.split('.')[-1]};base64,{base64_data}"
        except Exception:
            return None
