from django.utils import timezone
from rest_framework import serializers
from .models import Booking


class PublicBookingSerializer(serializers.ModelSerializer):
    """
    Serializer for publicly displaying booking information.
    It exposes non-sensitive details like check-in/out dates and guest count.
    """

    class Meta:
        model = Booking
        fields = (
            "pk",
            "check_in",
            "check_out",
            "experience_time",
            "guests",
        )


class CreateRoomBookingSerializer(serializers.ModelSerializer):
    """
    Serializer for creating a new room booking.
    It validates the input data to ensure booking logic is sound
    (e.g., no booking in the past, check-out is after check-in).
    """

    # Explicitly define fields to ensure they are always treated as DateField for input.
    # This can also be helpful for adding extra validation or help_text in the future.
    check_in = serializers.DateField()
    check_out = serializers.DateField()

    class Meta:
        model = Booking
        fields = (
            "check_in",
            "check_out",
            "guests",
        )

    def validate(self, data):
        """
        Perform cross-field validation for the booking dates.
        This method is automatically called by DRF during validation.
        'data' is a dictionary of the validated field values.
        """
        # 1. Check if check_out date is after check_in date.
        # This is a critical business rule for any booking system.
        if data["check_out"] <= data["check_in"]:
            # Raise a non-field error or attach to a specific field.
            # Attaching to 'check_out' provides a clearer error message to the client.
            raise serializers.ValidationError(
                {"check_out": "Check-out date must be after the check-in date."}
            )

        # 2. Check if the check_in date is in the past.
        today = timezone.localtime(timezone.now()).date()
        if data["check_in"] < today:
            raise serializers.ValidationError(
                {"check_in": "Cannot create a booking for a past date."}
            )

        # 3.
        if Booking.objects.filter(
            check_in__lte=data["check_out"],
            check_out__gte=data["check_in"],
        ).exists():
            raise serializers.ValidationError(
                "Those (or some) of those dates are already taken."
            )

        # If all validations pass, return the data.
        # There's no need to check if 'check_out' is in the past,
        # because if 'check_in' is today or in the future, and 'check_out'
        # is after 'check_in', 'check_out' cannot be in the past.
        return data
