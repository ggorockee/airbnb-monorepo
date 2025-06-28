from rest_framework import serializers
from .models import Amenity, Room
from user.serializers import TinyUserSerializer
from review.serializers import ReviewSerializer
from category.seirializers import CategorySerializer
from wishlist.models import Wishlist


class AmenitySerializer(serializers.ModelSerializer):
    """
    Serializer for the Amenity model.
    Used to represent amenities like "Wi-Fi", "Pool", etc.
    """

    class Meta:
        model = Amenity
        fields = (
            "name",
            "description",
        )


class RoomListSerializer(serializers.ModelSerializer):
    """
    Serializer for displaying a simplified list of rooms.
    This is optimized for list views to avoid sending excessive data.
    """

    # A read-only field that calculates the room's average rating.
    rating = serializers.SerializerMethodField()
    # A read-only field that represents the primary photos of the room.
    # photos = PhotoSerializer(many=True, read_only=True)

    class Meta:
        model = Room
        fields = (
            "pk",
            "name",
            "country",
            "city",
            "price",
            "rating",
            "photos",
        )

    def get_rating(self, room):
        """Calculates and returns the average rating for a room."""
        return room.rating()


class RoomDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for the detailed view of a single Room object.
    It includes nested representations of related objects like owner, amenities, etc.
    """

    # --- Nested Serializers for Related Objects ---
    # Represents the owner of the room using a simplified user serializer. Read-only.
    owner = TinyUserSerializer(read_only=True)
    # Represents the list of amenities available in the room. Read-only.
    amenities = AmenitySerializer(read_only=True, many=True)
    # Represents the category of the room (e.g., "House", "Apartment"). Read-only.
    category = CategorySerializer(read_only=True)
    # Represents all photos associated with the room. Read-only.
    # photos = PhotoSerializer(many=True, read_only=True)

    # --- Custom Fields computed at runtime ---
    # A read-only field that calculates the room's average rating.
    rating = serializers.SerializerMethodField()
    # A read-only boolean field indicating if the requesting user is the owner of the room.
    is_owner = serializers.SerializerMethodField()
    # A read-only boolean field indicating if the requesting user has "liked" (wishlisted) this room.
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Room
        # "__all__" includes all fields from the Room model.
        fields = "__all__"
        # For better readability, you could also explicitly list all fields:
        # fields = (
        #     "pk", "name", "country", "city", "price", "rooms", "toilets",
        #     "description", "address", "pet_friendly", "kind", "owner",
        #     "amenities", "category", "created_at", "updated_at", "rating",
        #     "is_owner", "is_liked", "photos",
        # )

    def get_rating(self, room):
        """
        Computes and returns the average rating for the room.
        This method is called to populate the 'rating' field.
        """
        return room.rating()

    def get_is_owner(self, room):
        """
        Checks if the user making the request is the owner of the room.
        Requires 'request' to be passed in the serializer's context.
        Returns True if the user is the owner, otherwise False.
        """
        request = self.context.get("request")
        if request:
            return room.owner == request.user
        return False

    def get_is_liked(self, room):
        """
        Checks if the room is in the wishlist of the user making the request.
        Requires 'request' to be passed in the serializer's context.
        Returns True if the room is on the user's wishlist, otherwise False.
        """
        request = self.context.get("request")
        # Check if the user is authenticated before querying the database.
        if request and request.user.is_authenticated:
            # A highly efficient query to check for the existence of a record.
            return Wishlist.objects.filter(
                user=request.user,
                rooms__pk=room.pk,  # Check for the room's pk in the 'rooms' many-to-many relationship.
            ).exists()
        return False
