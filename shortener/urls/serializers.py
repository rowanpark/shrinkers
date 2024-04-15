from django.contrib.auth.models import User

from rest_framework import serializers

from shortener.models import ShortenedUrls, Users
from shortener.utils import url_count_changer


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
        # fields = ['id', 'nick_name', 'prefix', 'target_url', 'shortened_url', 'click', 'creator', 'created_via', 'expired_at']
        fields = '__all__'  # 모든 필드


class UrlCreateSerializer(serializers.Serializer):
    nick_name = serializers.CharField(max_length=50)
    category = serializers.IntegerField(required=False)
    target_url = serializers.CharField(max_length=2000)

    def create(self, request, data, commit=True):
        print('data:', data)
        instance = ShortenedUrls()
        instance.creator_id = request.user.id
        instance.nick_name = data.get('nick_name', None)
        instance.category = data.get('category', None)
        # instance.target_url = data.get('target_url', None).strip()  # None 허용
        instance.target_url = data.get('target_url').strip()  # None 비허용
        if commit:
            try:
                instance.save()
            except Exception as e:
                print('UrlCreateSerializer Error:', e)
            else:
                url_count_changer(request, True)
        print('instance:', instance)
        return instance
