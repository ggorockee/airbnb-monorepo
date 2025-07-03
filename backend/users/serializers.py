from rest_framework.exceptions import ValidationError
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password


class TinyUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = (
            "email",
            "username",
        )


class PrivateUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        # List all fields you want for user creation and display.
        # Ensure 'password' is included for input but handled separately.
        # fields = (
        #     "pk",
        #     "username",
        #     "email",
        #     "password",  # Password will be write-only
        # )
        # extra_kwargs = {
        #     "password": {
        #         "write_only": True,  # Ensures password is not sent back in the response.
        #         "style": {
        #             "input_type": "password"
        #         },  # Hides password input in the browsable API.
        #     }
        # }
        exclude = (
            "password",
            "is_superuser",
            "id",
            "is_staff",
            "is_active",
            "first_name",
            "last_name",
            "groups",
            "user_permissions",
        )

    def create(self, validated_data):
        """
        Overrides the default create method to handle password hashing.
        This is the standard and secure way to create users with DRF.
        """
        # Remove the plain-text password from the validated data dictionary.
        password = validated_data.pop("password")

        # Create the user instance with the remaining data.
        # The '**' operator unpacks the dictionary into keyword arguments.
        user = get_user_model().objects.create(**validated_data)

        # Use set_password() to hash the password and then save the user.
        user.set_password(password)
        user.save()

        return user


class PublicUserSerializer(serializers.ModelSerializer):
    """
    Serializer for displaying a user's public-facing profile.
    It deliberately exposes only non-sensitive information.
    """

    class Meta:
        model = get_user_model()
        # Only include fields that are safe to be viewed by anyone.
        # NEVER include fields like 'email', 'first_name', 'last_name', etc.
        fields = (
            "email",
            "username",
        )


class PasswordChangeSerializer(serializers.Serializer):
    """
    Serializer for password change endpoint.
    This serializer handles all the validation logic for changing a user's password.
    """

    old_password = serializers.CharField(
        write_only=True,
        required=True,
        style={"input_type": "password"},
    )
    new_password = serializers.CharField(
        write_only=True,
        required=True,
        style={"input_type": "password"},
    )

    def validate_old_password(self, value):
        """
        Validates that the old password is correct for the current user.
        """
        # The user is retrieved from the context passed by the view.
        user = self.context["request"].user
        if not user.check_password(value):
            # Raise a specific, clear error message.
            raise ValidationError("Incorrect old password.")
        return value

    def validate(self, data):
        """
        Ensures the new password meets Django's password validation criteria.
        """
        # Django's password validators can be used here.
        # It checks for things like minimum length, common sequences, etc.
        try:
            validate_password(data["new_password"], self.context["request"].user)
        except ValidationError as e:
            # The error messages from Django's validators are returned.
            raise serializers.ValidationError({"new_password": list(e.messages)})
        return data

    def save(self, **kwargs):
        """
        Sets the new password on the user object and saves it.
        """
        user = self.context["request"].user
        new_password = self.validated_data["new_password"]
        user.set_password(new_password)
        user.save()
        return user
