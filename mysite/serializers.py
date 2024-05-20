from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Profile


class ProfileSearializer(serializers.ModelSerializer):
    users = serializers.HyperlinkedRelatedField(view_name='user-detail', read_only=True)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Profile
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    profiles = serializers.HyperlinkedRelatedField(view_name='profile-detail', read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'profiles']
