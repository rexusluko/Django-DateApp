import base64

from rest_framework import serializers
from .models import CustomUser, ZodiacSign
from django.core.files.base import ContentFile
from .photo import load_photo_from_minio


class UserSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255)
    gender = serializers.CharField(max_length=255)
    email = serializers.CharField(max_length=255)
    zodiac_sign = serializers.CharField(max_length=255)
    description = serializers.CharField(max_length=255)
    photo_path = serializers.CharField(max_length=255)

    def create(self, validated_data):
        zodiac_name = validated_data.pop('zodiac_sign')
        zodiac_sign = ZodiacSign.objects.get(name=zodiac_name)
        user = CustomUser.objects.create_user(zodiac_sign=zodiac_sign, **validated_data)
        return user


class ImageFieldFromMinio(serializers.ImageField):
    def to_representation(self, value):
        if value:
            try:
                photo_data = load_photo_from_minio(value)  # Загрузка данных из MinIO
                photo_file = ContentFile(photo_data, name=value)
                return super().to_representation(photo_file)
            except Exception as e:
                return None
        return None

class MostCompatibleUserSerializer(serializers.ModelSerializer):
    zodiac_sign = serializers.CharField(source='zodiac_sign.name')
    photo = serializers.SerializerMethodField()  # Добавляем новое поле photo

    class Meta:
        model = CustomUser
        fields = ('id','username', 'gender', 'zodiac_sign', 'description', 'photo', 'email')

    def get_photo(self, obj):
        if obj.photo_path != 'no photo':
            binary_data = load_photo_from_minio(obj.photo_path)
            base64_data = base64.b64encode(binary_data).decode('utf-8')
            return 'data:image/png;base64,' + base64_data
        return None


class LikeUserSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()

class DislikeUserSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()