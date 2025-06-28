from rest_framework import status
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from media.models import Photo


class PhotoDetail(APIView):
    """
    API View to handle details of a specific Photo object.
    Requires authentication for all methods.
    """

    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        """
        Helper method to retrieve a Photo object by its primary key (pk).
        Raises a NotFound (404) error if the photo does not exist.
        """
        try:
            return Photo.objects.get(pk=pk)
        except Photo.DoesNotExist:
            raise NotFound(detail="Photo not found.")

    def delete(self, request, pk):
        """
        Handles DELETE requests to delete a specific photo.
        """
        # First, retrieve the photo object using the helper method.
        # If not found, it will raise a 404 error automatically.
        photo = self.get_object(pk)

        # Check for ownership. The user can only delete a photo if they own the associated Room or Experience.
        # This is a critical security check to prevent users from deleting others' photos.
        is_room_photo_and_not_owner = photo.room and photo.room.owner != request.user
        is_experience_photo_and_not_owner = (
            photo.experience and photo.experience.host != request.user
        )

        if is_room_photo_and_not_owner or is_experience_photo_and_not_owner:
            # If the user is not the owner, raise a PermissionDenied (403 Forbidden) error.
            # Added a custom detail message for clarity.
            raise PermissionDenied(
                detail="You do not have permission to delete this photo."
            )

        # If the ownership check passes, delete the photo object from the database.
        photo.delete()

        # For a successful DELETE operation, it's a best practice to return a 204 No Content status.
        # This indicates that the action was successful, and there is no content to return in the response body.
        return Response(status=status.HTTP_204_NO_CONTENT)
