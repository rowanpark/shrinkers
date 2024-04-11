from django.contrib.auth.models import User

from rest_framework import serializers

from shortener.models import ShortenedUrls, Users


class UserBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('password',)


class UserSerializer(serializers.ModelSerializer):
    user = UserBaseSerializer(read_only=True)

    class Meta:
        model = Users
        fields = ['id', 'url_count', 'organization', 'user']


class UrlListSerializer(serializers.ModelSerializer):
    creator = UserSerializer(read_only=True)

    class Meta:
        model = ShortenedUrls
        fields = ['id', 'nick_name', 'prefix', 'target_url', 'shortened_url', 'click', 'creator', 'created_via', 'expired_at']
        # fields = '__all__'  # 모든 필드
