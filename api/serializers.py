from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Category, Blog, Comment, FAQ, Tag

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'first_name', 'last_name')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        return user

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

class BlogSerializer(serializers.ModelSerializer):
    author_name = serializers.ReadOnlyField(source='author.username')
    category_name = serializers.ReadOnlyField(source='category.name')
    tag_names = serializers.StringRelatedField(many=True, source='tags', read_only=True)

    class Meta:
        model = Blog
        fields = ('id', 'title', 'slug', 'author', 'author_name', 'category', 'category_name', 'tags', 'tag_names', 'content', 'created_at', 'updated_at', 'status')
        read_only_fields = ('author', 'slug', 'tag_names', 'tags')

    def create(self, validated_data):
        from django.db import IntegrityError
        from rest_framework.exceptions import ValidationError
        
        # Handle tags from request data
        tag_names = self.context['request'].data.get('tags', [])
        
        try:
            blog = Blog.objects.create(**validated_data)
        except IntegrityError:
            raise ValidationError({'title': ['A blog with this title already exists.']})
            
        if tag_names:
            tag_objs = []
            for name in tag_names:
                name = name.strip()
                if name:
                    tag, _ = Tag.objects.get_or_create(name=name)
                    tag_objs.append(tag)
            blog.tags.set(tag_objs)
        return blog

    def update(self, instance, validated_data):
        from django.db import IntegrityError
        from rest_framework.exceptions import ValidationError
        
        tag_names = self.context['request'].data.get('tags', None)
        
        try:
            instance = super().update(instance, validated_data)
        except IntegrityError:
            raise ValidationError({'title': ['A blog with this title already exists.']})
            
        if tag_names is not None:
            tag_objs = []
            for name in tag_names:
                name = name.strip()
                if name:
                    tag, _ = Tag.objects.get_or_create(name=name)
                    tag_objs.append(tag)
            instance.tags.set(tag_objs)
        return instance

class CommentSerializer(serializers.ModelSerializer):
    user_name = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Comment
        fields = ('id', 'blog', 'user', 'user_name', 'content', 'created_at')
        read_only_fields = ('user',)

class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = '__all__'
