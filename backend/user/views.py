from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, get_user_model, logout, login
from django.shortcuts import get_object_or_404


from rest_framework.exceptions import (
    AuthenticationFailed,
)  # Import AuthenticationFailed

from rest_framework.permissions import IsAuthenticated
from . import serializers

# Import the RefreshToken model from simple-jwt
from rest_framework_simplejwt.tokens import RefreshToken

# It's good practice to use a serializer for user data
from .serializers import TinyUserSerializer, PasswordChangeSerializer


class LoginView(APIView):
    """
    API View for user login.
    Authenticates user credentials and returns JWT tokens and user data.
    """

    def post(self, request):
        # Extract email and password from the request data
        email = request.data.get("email")
        password = request.data.get("password")

        # check if email or password was not provided
        if not email or not password:
            return Response(
                data={"error": "Both email and password are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Authenticated the user using Django's built-in function
        # `authenticate` returns the user object if credentials are valid, otherwise None.
        user = authenticate(username=email, password=password)
        # check if autheication was successful
        if user is not None:
            # If the user is authenticated, generate JWT tokens
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)

            # serialize the user data
            user_serializer = TinyUserSerializer(user)

            # Prepare the response data
            response_data = {
                "message": "Login successful",
                "user": user_serializer.data,
                "access_token": access_token,
                "refresh_token": str(refresh),
            }
            login(request, user)
            return Response(response_data, status=status.HTTP_200_OK)

        raise AuthenticationFailed("Invalid credentials, please try again.")


class ChangePassword(APIView):
    """
    API View for allowing an authenticated user to change their password.
    """

    permission_classes = [IsAuthenticated]

    def put(self, request):
        """
        Handles PUT requests to change the user's password.
        The view's role is now simply to pass data and context to the serializer.
        """
        # Pass request to the serializer's context to access the user.
        serializer = PasswordChangeSerializer(
            data=request.data,
            context={"request": request},
        )

        # The serializer now handles all validation, including checking
        # the old password and validating the new one.
        # If invalid, a 400 response with clear error messages is returned.
        serializer.is_valid(raise_exception=True)

        # The serializer's save method contains the logic to set the new password.
        serializer.save()

        return Response(
            {"ok": "Password changed successfully."}, status=status.HTTP_200_OK
        )


class LogoutView(APIView):
    """
    API View for logging out a user.
    This action invalidates the user's session.
    """

    # Ensures that only authenticated users can access this endpoint.
    # An unauthenticated user has no session to log out from.
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        Handles POST requests to log out the current user.

        We use POST for this action because logging out is a state-changing
        operation on the server. Using POST helps prevent Cross-Site Request Forgery (CSRF)
        vulnerabilities that could arise if a GET request were used.
        """
        # The `logout` function from django.contrib.auth handles the process
        # of clearing the user's session data from the server.
        logout(request)

        # Return a success response. It's good practice to provide a clear
        # message. The status code 200 OK is appropriate.
        return Response(
            {"ok": "Successfully logged out."},
            status=status.HTTP_200_OK,
        )


class PublicUser(APIView):
    """
    API View to display a user's public profile information.
    """

    def get(self, request, username):
        """
        Handles GET requests to retrieve a user's public profile
        by their username.
        """
        # Use the get_object_or_404 shortcut to fetch the user.
        # It's a cleaner and more standard way to handle the "Not Found" case.
        # If a user with the given username doesn't exist, it automatically
        # returns a 404 Not Found response.
        user = get_object_or_404(get_user_model(), username=username)

        # Use the dedicated PublicUserSerializer to ensure no sensitive
        # data is ever exposed on this public endpoint.
        serializer = serializers.PublicUserSerializer(user)

        return Response(serializer.data)


class Me(APIView):
    """
    An endpoint for the currently authenticated user to view and edit their profile.
    """

    # Ensures that only logged-in users can access this view.
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Handles GET requests to retrieve the profile of the authenticated user.
        """
        # request.user directly provides the authenticated user model instance.
        user = request.user
        # The PrivateUserSerializer is used to include all user details,
        # including private information, suitable for the user themself.
        serializer = serializers.PrivateUserSerializer(user)
        return Response(serializer.data)

    def put(self, request):
        """
        Handles PATCH requests to partially update the authenticated user's profile.

        Using PATCH is more semantically correct than PUT for partial updates.
        """
        # The user instance to be updated is the one making the request.
        user = request.user

        # Instantiate the serializer with:
        # 1. The user instance to update.
        # 2. The new data from the request.
        # 3. partial=True to allow for updating only a subset of fields.
        serializer = serializers.PrivateUserSerializer(
            user,
            data=request.data,
            partial=True,
        )

        # Validate the request data. Raises a validation error if invalid.
        serializer.is_valid(raise_exception=True)

        # Save the updated user data. The serializer's save() method
        # will call the update() method on the User model instance.
        serializer.save()

        # Return the updated user data directly from the same serializer.
        # There is no need to re-serialize the object.
        # A successful update returns a 200 OK status code by default.
        return Response(serializer.data)


class Users(APIView):
    """
    API View for creating a new user (i.e., user registration).
    """

    def post(self, request):
        """
        Handles POST requests to create a new user account.
        """
        # All validation and creation logic is now handled by the serializer.
        # The view's responsibility is simply to pass data to the serializer.
        serializer = serializers.PrivateUserSerializer(data=request.data)

        # Validate data. If 'password' is missing or other rules fail,
        # an exception is raised and a 400 response is returned automatically.
        serializer.is_valid(raise_exception=True)

        # serializer.save() will now trigger the custom 'create' method
        # that we defined in the serializer, which handles password hashing.
        serializer.save()

        # Return the data from the serializer (which won't include the password)
        # and a '201 Created' status.
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
        )
