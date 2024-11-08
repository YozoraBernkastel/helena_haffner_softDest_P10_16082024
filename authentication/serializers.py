from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from authentication.models import User


class CreateUserSerializer(ModelSerializer):
    password = serializers.CharField(write_only=True)

    # birthday_date = serializers.DateField(write_only=True)
    # can_contact = serializers.BooleanField(write_only=True)
    # share_personal_data = serializers.BooleanField(write_only=True)

    def create(self, validated_data):
        contributor = User.objects.create_user(username=validated_data["username"],
                                               password=validated_data["password"],
                                               birthday_date=validated_data["birthday_date"],
                                               can_contact=validated_data["can_contact"],
                                               share_personal_data=validated_data["share_personal_data"]
                                               )
        return contributor

    class Meta:
        model = User
        fields = ["username", "password", "birthday_date", "can_contact", "share_personal_data"]


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "birthday_date", "can_contact", "share_personal_data"]

    birthday_date = serializers.DateField(write_only=True)
    can_contact = serializers.BooleanField(write_only=True)
    share_personal_data = serializers.BooleanField(write_only=True)
