import base64
import uuid
import six
import filetype
from rest_framework import serializers
from django.core.files.base import ContentFile

class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if not data:
            raise serializers.ValidationError('Поле image обязательно.')
        
        if isinstance(data, str) and data.startswith('data:image'):
            # Извлекаем расширение из MIME-типа
            mime_type, base64_data = data.split(';base64,')
            file_extension = mime_type.split('/')[-1]  # 'jpeg', 'png' и т.д.
            
            try:
                decoded_file = base64.b64decode(base64_data)
            except (TypeError, binascii.Error):
                raise serializers.ValidationError('Некорректное base64 изображение.')
            
            file_name = f"{uuid.uuid4()}.{file_extension}"
            return ContentFile(decoded_file, name=file_name)
        
        return super().to_internal_value(data)

    def to_representation(self, value):
        if not value:
            return None
            
        request = self.context.get('request')
        try:
            return request.build_absolute_uri(value.url) if request else value.url
        except ValueError:
            return None