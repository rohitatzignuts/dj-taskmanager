from rest_framework import serializers
from mytasks.models import Task
from django.contrib.auth.models import User


class TaskSerializer(serializers.ModelSerializer):
    due_date = serializers.DateField(format="%d-%m-%Y")

    class Meta:
        model = Task
        fields = ["id", "title", "description", "due_date", "priority", "is_completed"]


class UserSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "password1", "password2"]

    def validate(self, data):
        if data["password1"] != data["password2"]:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        return data

    def create(self, validated_data):
        validated_data.pop("password2")
        user = User(
            username=validated_data["username"],
            first_name=validated_data.get("first_name", ""),
            last_name=validated_data.get("last_name", ""),
        )
        user.set_password(validated_data["password1"])
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(write_only=True)
