import base64
import uuid
import six
import filetype
from rest_framework import serializers
from django.core.files.base import ContentFile

class Base64ImageField(serializers.ImageField):

    def to_representation(self, value):
        request = self.context.get('request', None)
        if not value:
            return None
        try:
            return request.build_absolute_uri(value.url) if request else value.url
        except Exception:
            return None

    def to_internal_value(self, data):
        if data in [None, '']:
            raise serializers.ValidationError('Поле image обязательно.')
        
        if isinstance(data, six.string_types):
            if 'data:' in data and ';base64,' in data:
                header, data = data.split(';base64,')
            try:
                decoded_file = base64.b64decode(data)
            except TypeError:
                self.fail('invalid_image')

            file_name = str(uuid.uuid4())[:12]
            file_extension = 'jpg'  # Можно улучшить: определять расширение по header
            complete_file_name = f"{file_name}.{file_extension}"

            return ContentFile(decoded_file, name=complete_file_name)

        return super().to_internal_value(data)

    def get_file_extension(self, file_name, decoded_file):
        kind = filetype.guess(decoded_file)
        if kind is None:
            return 'jpg'
        return kind.extension