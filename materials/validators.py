from urllib.parse import urlparse

from rest_framework import serializers


def validate_youtube_url(value):
    parsed_url = urlparse(value)

    if parsed_url.scheme not in ('http', 'https'):
        raise serializers.ValidationError(
            'Ссылка должна использовать HTTP или HTTPS.'
        )

    hostname = parsed_url.hostname

    if hostname:
        hostname = hostname.lower()

    if hostname not in ('youtube.com', 'www.youtube.com'):
        raise serializers.ValidationError(
            'Разрешены только ссылки на youtube.com.'
        )

    return value