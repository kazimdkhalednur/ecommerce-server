from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from .models import User


class UserDataSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "username",
            "email",
            "role",
        ]


class CreateUserSerializer(ModelSerializer):
    password2 = serializers.CharField(style={"input_type": "password"}, write_only=True)

    class Meta:
        model = User
        fields = ["username", "email", "password", "password2"]
        extra_kwargs = {"password": {"write_only": True}}

    def save(self, **kwargs):
        user = User(
            email=self.validated_data["email"],
            username=self.validated_data["username"],
            **kwargs
        )
        password = self.validated_data["password"]
        password2 = self.validated_data["password2"]

        if password != password2:
            raise serializers.ValidationError({"error": "Passwords do not match."})
        user.set_password(password)
        user.save()
        return user


class PasswordChangeSerializer(serializers.Serializer):
    current_password = serializers.CharField(
        style={"input_type": "password"}, required=True
    )
    new_password = serializers.CharField(
        style={"input_type": "password"}, required=True
    )
    confirm_password = serializers.CharField(
        style={"input_type": "password"}, required=True
    )

    def validate_current_password(self, value):
        if not self.context["request"].user.check_password(value):
            raise serializers.ValidationError({"error": "Incorrect Password"})
        return value

    def save(self):
        new_password = self.validated_data["new_password"]
        confirm_password = self.validated_data["confirm_password"]
        if new_password != confirm_password:
            raise serializers.ValidationError({"error": "Passwords do not match."})
        user = User.objects.get(id=self.context.get("request").user.id)
        user.set_password(new_password)
        user.save()
        return user


class EmailChangeSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(style={"input_type": "password"}, write_only=True)

    def validate_password(self, value):
        if not self.context["request"].user.check_password(value):
            raise serializers.ValidationError({"error": "Incorrect Password"})
        return value


class PasswordCheckSerializer(serializers.Serializer):
    password = serializers.CharField(style={"input_type": "password"}, write_only=True)

    def validate_password(self, value):
        if not self.context["request"].user.check_password(value):
            raise serializers.ValidationError({"error": "Incorrect Password"})
        return value


class PasswordResetEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError({"error": "User doesn't exists"})
        return value


class PasswordResetSerializer(serializers.Serializer):
    new_password = serializers.CharField(
        style={"input_type": "password"}, required=True
    )
    confirm_password = serializers.CharField(
        style={"input_type": "password"}, required=True
    )

    def save(self):
        new_password = self.validated_data["new_password"]
        confirm_password = self.validated_data["confirm_password"]
        if new_password != confirm_password:
            raise serializers.ValidationError({"error": "Passwords do not match."})
        user = self.context.get("user")
        user.set_password(new_password)
        user.save()
        return user
