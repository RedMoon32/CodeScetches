from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers

from profile.models import UserProfile
from innopoints import settings


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, max_length=50)
    password = serializers.CharField(required=True, max_length=50)

    def validate(self, attrs):
        email = attrs['email']
        password = attrs['password']

        user = authenticate(username=email, password=password)

        if user:
            attrs['user'] = user
            return attrs
        else:

            raise serializers.ValidationError("User is not authenticated")


class ProfileSerializer(serializers.ModelSerializer):
    permissions = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = ('name', 'surname', 'points', 'xp', 'permissions')

    def get_permissions(self, profile):
        all_permissions = User(is_superuser=True).get_all_permissions()
        all_permissions = [perm for perm in all_permissions if perm.startswith(tuple(settings.DJANGO_APPS))]
        user_permissions = profile.user.get_all_permissions()

        return {p: p in user_permissions for p in all_permissions}
