from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user object"""

    class Meta:
        model = get_user_model()
        fields = ["id" , "username" , "email", "password"]
        extra_kwargs = {
            "password": {"write_only": True, "min_length": 5},
            "id": {"read_only" : True}
            }

    def create(self, validated_data):
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()
        return user

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        if instance.is_superuser:
            representation["admin"] = True
        return representation
