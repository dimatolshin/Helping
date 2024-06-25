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


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'username', 'id']


class RelationshipSerializer(serializers.ModelSerializer):
    parent = serializers.PrimaryKeyRelatedField(many=True, queryset=Profile.objects.all(), default=[])
    children = serializers.PrimaryKeyRelatedField(many=True, queryset=Profile.objects.all(), default=[])
    requests_to_parents = serializers.PrimaryKeyRelatedField(many=True, queryset=Profile.objects.all(), default=[])
    requests_to_childrens = serializers.PrimaryKeyRelatedField(many=True, queryset=Profile.objects.all(), default=[])
    owner = serializers.PrimaryKeyRelatedField(many=True, queryset=Profile.objects.all(), default=[])

    class Meta:
        model = Relationship
        fields = '__all__'


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'

    def validate_children(self, value):
        if value != 'Ребёнок':
            raise serializers.ValidationError({'Error': 'Отказано в доступе'})
        return value

    def validate_text(self, value):
        if not value:
            raise serializers.ValidationError({'text': 'Строчка не может быть пустой'})
        return value


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

    def validate_text(self, value):
        if not value:
            raise serializers.ValidationError({'text': 'Строчка не может быть пустой'})
        return value


class CommentSerializer(serializers.ModelSerializer):
    profile = serializers.HiddenField(default=serializers.CurrentUserDefault())
    like_list = serializers.PrimaryKeyRelatedField(many=True, queryset=Profile.objects.all(), default=[])

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('like_list', 'like')

    def validate_text(self, value):
        if not value:
            raise serializers.ValidationError({'text': 'Строчка не может быть пустой'})
        return value


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

    def validate_text(self, value):
        if not value:
            raise serializers.ValidationError({'text': 'Строчка не может быть пустой'})
        return value


class RoomSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Room
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

    def validate_name(self, value):
        if not value:
            raise serializers.ValidationError({'text': 'Строчка не может быть пустой'})
        return value


class PodCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PodCategory
        fields = '__all__'

    def validate_name(self, value):
        if not value:
            raise serializers.ValidationError({'text': 'Строчка не может быть пустой'})
        return value


class PictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Picture
        fields = '__all__'


class CalendarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Calendar
        fields = '__all__'

    def validate_parent(self, value):
        if value != 'Родитель':
            raise serializers.ValidationError({'Error': 'Отказано в доступе'})
        return value


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

    def validate_parent(self, value):
        if value != 'Родитель':
            raise serializers.ValidationError({'Error': 'Отказано в доступе'})
        return value

    def validate_expert(self, value):
        if value != 'Эксперт':
            raise serializers.ValidationError({'Error': 'Отказано в доступе'})
        return value


class TimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Time
        fields = '__all__'
