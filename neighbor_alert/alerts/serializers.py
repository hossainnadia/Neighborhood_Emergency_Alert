from rest_framework import serializers
from .models import User, Emergency, Post, Comment


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'phone', 'location', 'latitude', 'longitude', 'role']


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'phone', 'location']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            phone=validated_data.get('phone', ''),
            location=validated_data.get('location', '')
        )
        return user


class CommentSerializer(serializers.ModelSerializer):
    user_username = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Comment
        fields = ['id', 'post', 'user', 'user_username', 'text', 'created_at']
        read_only_fields = ['user']


class EmergencySerializer(serializers.ModelSerializer):
    user_details = UserSerializer(source='user', read_only=True)

    class Meta:
        model = Emergency
        fields = '__all__'
        read_only_fields = ['user']


class PostSerializer(serializers.ModelSerializer):
    user_details = UserSerializer(source='user', read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = '__all__'
        read_only_fields = ['user', 'created_at']
        extra_kwargs = {
            'location': {'required': False, 'allow_blank': True, 'allow_null': True},
            'status': {'required': False, 'default': 'Active'},
        }