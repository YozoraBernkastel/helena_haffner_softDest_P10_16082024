from rest_framework.serializers import ModelSerializer
from authentication.models import User


class UserSerializer(ModelSerializer):
    def create(self, validated_data):
        contributor = User.objects.create(username=validated_data["username"],
                                          password=validated_data["password"],
                                          birthday_date=validated_data["birthday_date"],
                                          can_contact=validated_data["can_contact"],
                                          share_personal_data=validated_data["share_personal_data"]
                                          )
        return contributor

    class Meta:
        model = User
        fields = ["user", "project", "time_created"]
