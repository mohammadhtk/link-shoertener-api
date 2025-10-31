from rest_framework import serializers
from .models import User


# Serializer for viewing User info
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


# Serializer for registering a new user
class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists")
        return value

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            email=validated_data['email'],
            role=User.USER  # default role is USER
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


# Serializer for user login
class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)


# Serializer for updating user details
class UserUpdateSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(
        choices=User.ROLE_CHOICES,
        required=False
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'role', 'is_active']

    def validate_role(self, value):
        # ensure role is valid
        valid_roles = [choice[0] for choice in User.ROLE_CHOICES]
        if value not in valid_roles:
            raise serializers.ValidationError(f"Role '{value}' does not exist")
        return value

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            if attr == 'role':
                instance.role = value
            else:
                setattr(instance, attr, value)
        instance.save()
        return instance


# Serializer for returning JWT tokens and user info
class LoginResponseSerializer(serializers.Serializer):
    access = serializers.CharField()
    refresh = serializers.CharField()
    user = UserSerializer()
