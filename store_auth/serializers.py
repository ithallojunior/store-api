from rest_framework import serializers

from django.contrib.auth.models import User
from django.contrib.auth.password_validation import (
    get_password_validators,
    validate_password,
)
from django.conf import settings


class UserSerializer(serializers.ModelSerializer):
    """Serializer to deal with user creation, update, and deletion."""

    def validate_password(self, password):
        """Validating it to django set policies."""

        # validate the password against existing validators
        validate_password(
            password,
            user=None,
            password_validators=get_password_validators(
                getattr(settings, 'AUTH_PASSWORD_VALIDATORS', None)
            )
        )

        return password

    def create(self, validated_data):
        raw_password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(raw_password)
        user.save()

        # adding an empty field for password after setting it up
        validated_data['password'] = None
        return validated_data

    def update(self, instance, validated_data):

        if 'password' in validated_data.keys():
            raw_password = validated_data.pop('password')
            instance.set_password(raw_password)
            instance.save()

        super().update(instance, validated_data)

        # adding an empty field for password after setting it up
        validated_data['password'] = None
        return validated_data

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'password',
        ]
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
            'email': {'required': True},
        }
