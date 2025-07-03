from rest_framework import status  # Import status for explicit status codes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Wishlist
from .serializers import WishlistSerializer


class Wishlists(APIView):
    """
    API View to handle the collection of wishlists for the authenticated user.
    - GET: Retrieves all wishlists belonging to the user.
    - POST: Creates a new wishlist for the user.
    """

    # Ensures that only authenticated (logged-in) users can access this view.
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Handles GET requests to retrieve all wishlists for the currently logged-in user.
        """
        # Filter the Wishlist objects to get only those that belong to the requesting user.
        # This is a crucial step to ensure users can only see their own data.
        all_wishlists = Wishlist.objects.filter(user=request.user)

        # Serialize the queryset of wishlists.
        # - `many=True` is required because we are serializing a list of objects, not a single instance.
        # - `context={"request": request}` is passed to the serializer, which is often necessary
        #   for hyperlinked fields (e.g., to generate full URLs for related resources).
        serializer = WishlistSerializer(
            all_wishlists,
            many=True,
            context={"request": request},
        )

        # Return the serialized data with a 200 OK status, indicating a successful request.
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """
        Handles POST requests to create a new wishlist for the currently logged-in user.
        """
        # Instantiate the serializer with the data sent in the request body.
        serializer = WishlistSerializer(data=request.data)

        # Validate the incoming data against the serializer's rules.
        if serializer.is_valid():
            # If validation is successful, save the new object to the database.
            # We explicitly pass the `user` from the request object to the `save()` method.
            # This ensures the new wishlist is correctly associated with the authenticated user,
            # preventing users from creating wishlists for others.
            wishlist = serializer.save(user=request.user)

            # To provide a complete representation of the newly created object,
            # we re-serialize the `wishlist` instance.
            response_serializer = WishlistSerializer(
                wishlist,
                context={
                    "request": request
                },  # Pass context here as well for consistency
            )

            # Return the data of the newly created wishlist with a 201 Created status.
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        else:
            # If validation fails, return the error details provided by the serializer.
            # A 400 Bad Request status code indicates that the client's request was malformed.
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
