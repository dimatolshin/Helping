from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.decorators import action
from rest_framework.validators import UniqueValidator

from .models import *

UserModel = get_user_model()


class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Profile
        fields = '__all__'


# class RegisterSerializer(serializers.ModelSerializer):
#     email = serializers.EmailField(
#         required=True,
#         validators=[UniqueValidator(queryset=User.objects.all())]
#     )
#     password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
#     password2 = serializers.CharField(write_only=True, required=True)
#
#     class Meta:
#         model = User
#         fields = ('username', 'password', 'password2', 'email')
#         extra_kwargs = {
#             'first_name': {'required': True},
#             'last_name': {'required': True}
#         }
#
#     def validate(self, attrs):
#         if attrs['password'] != attrs['password2']:
#             raise serializers.ValidationError({"password": "Password fields didn't match."})
#         return attrs
#
#     def create(self, validated_data):
#         user = User.objects.create(
#             username=validated_data['username'],
#             email=validated_data['email'],
#         )
#         user.set_password(validated_data['password'])
#         user.save()
#         return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'username', 'id']


class RelationshipSerializer(serializers.ModelSerializer):
    parent = serializers.PrimaryKeyRelatedField(many=True, queryset=Profile.objects.all(), default=[])
    children = serializers.PrimaryKeyRelatedField(many=True, queryset=Profile.objects.all(), default=[])
    requests_to_parents = serializers.PrimaryKeyRelatedField(many=True, queryset=Profile.objects.all(), default=[])
    requests_to_childrens = serializers.PrimaryKeyRelatedField(many=True, queryset=Profile.objects.all(), default=[])
    list_on_invite = serializers.PrimaryKeyRelatedField(many=True, queryset=Profile.objects.all(), default=[])

    class Meta:
        model = Relationship
        fields = '__all__'


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'


class ArticleAddLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['like_list', 'like']


class ArticleSerializer(serializers.ModelSerializer):
    profile = serializers.HiddenField(default=serializers.CurrentUserDefault())
    like_list = serializers.PrimaryKeyRelatedField(many=True, queryset=Profile.objects.all(), default=[])

    class Meta:
        model = Article
        fields = '__all__'
        read_only_fields = ('like_list', 'like')

    def create(self, validated_data):
        article = Article.objects.create(
            profile=self.context['request'].user.profile,
            name=validated_data['name'],
            text=validated_data['text'])
        article.save()
        return article

    def update(self, instance, validated_data):
        instance.profile = self.context['request'].user.profile
        instance.name = validated_data.get('name', instance.name)
        instance.text = validated_data.get('text', instance.text)
        instance.save()
        return instance


class CommentSerializer(serializers.ModelSerializer):
    profile = serializers.HiddenField(default=serializers.CurrentUserDefault())
    like_list = serializers.PrimaryKeyRelatedField(many=True, queryset=Profile.objects.all(), default=[])

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('like_list', 'like')


class CommentAddLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment

    fields = ['like_list', 'like']


class MessageSerializer(serializers.ModelSerializer):
    room = serializers.PrimaryKeyRelatedField(many=True, queryset=Room.objects.all(), default=[])
    created_at_formatted = serializers.SerializerMethodField()
    profile = ProfileSerializer()

    class Meta:
        model = Message
        fields = '__all__'

    def get_created_at_formatted(self, obj: Message):
        return obj.created_at.strftime("%d-%m-%Y %H:%M:%S")


class RoomSerializer(serializers.ModelSerializer):
    current_users = serializers.PrimaryKeyRelatedField(many=True, queryset=Profile.objects.all(), default=[])
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Room
        fields = '__all__'
