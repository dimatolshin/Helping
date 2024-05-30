from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.decorators import action
from rest_framework.validators import UniqueValidator

from .models import *

UserModel = get_user_model()


class ProfileSearializer(serializers.ModelSerializer):
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





# -------------------------------------------------------------------------------------------------------------
class TopicSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fileds = 'all'


class CommentAddLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fileds = ['like_list', 'like']

    def update(self, validated_data, pk):
        comment = Comment.objects.get(id=pk)
        profile = self.request.user.profile
        if profile in comment.like_list.all():
            comment.like -= 1
            comment.like_list.remove(profile)

        else:
            comment.like += 1
            comment.like_list.add(profile)
        comment.save()
        return comment


class CommentSerializer(serializers.ModelSerializer):
    profile = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Comment
        fileds = '__all__'

    def create(self, validated_data):
        return Comment.objects.create(**validated_data)

    def update(self, instance, validated_data, pk):
        article = Article.objects.get(id=pk)
        instance.profile = self.request.user.profile
        instance.article = article
        instance.text = validated_data.get('text', instance.text)
        instance.save()
        return instance


class RelationshipSerializer(serializers.ModelSerializer):
    #  owner=serializer.CurrentUserDefault()
    class Meta:
        model = Relationship
        fileds = ['request_to_parents', 'request_to_children', 'parent', 'children']

    def create(self, pk):
        user = self.request.user
        if user.profile.status == 'Родитель':
            request_to_parents = user
            request_to_children = Profile.objects.get(id=pk)
        else:
            request_to_parents = Profile.objects.get(id=pk)
            request_to_children = user
        return Relationship.objects.create(request_to_parents=request_to_parents,
                                           request_to_children=request_to_children)

    # def update(self, validated_data):
    #     relationship = Relationship.objects.get(


class ArticleAddLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['like_list', 'like']



class ArticleASerializer(serializers.ModelSerializer):
    profile = serializers.HiddenField(default=serializers.CurrentUserDefault())
    like_list = serializers.PrimaryKeyRelatedField(many=True, queryset=Profile.objects.all(), default=[])

    class Meta:
        model = Article
        fields = '__all__'

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

