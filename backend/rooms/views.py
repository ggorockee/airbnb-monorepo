from django.db import transaction
from django.shortcuts import get_object_or_404
from django.utils import timezone

from rest_framework.exceptions import (
    NotFound,
    NotAuthenticated,
    ParseError,
    PermissionDenied,
)
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.views import APIView
from rest_framework import status

from categories.models import Category
from reviews.serializers import ReviewSerializer
from rooms.models import Amenity, Room
from rooms.serializers import AmenitySerializer, RoomListSerializer, RoomDetailSerializer

from bookings.models import Booking
from bookings.serializers import PublicBookingSerializer, CreateRoomBookingSerializer


class Rooms(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        all_rooms = Room.objects.all()
        serializer = RoomListSerializer(
            all_rooms,
            many=True,
            context={"request": request},
        )

        return Response(serializer.data)

    def post(self, request):
        serializer = RoomDetailSerializer(data=request.data)
        if serializer.is_valid():
            category_pk = request.data.get("category")
            if not category_pk:
                raise ParseError("Category is a required field.")
            try:
                category = Category.objects.get(pk=category_pk)
                if category.kind == Category.CategoryKindChoices.EXPERIENCES:
                    raise ParseError(
                        "The selected category must be for rooms, not experiences."
                    )
            except Category.DoesNotExist:
                raise ParseError("Category not found.")

            # serializer.save() 시 owner와 category를 함께 전달
            try:
                with transaction.atomic():
                    room = serializer.save(
                        owner=request.user,
                        category=category,
                    )
                    amenities = request.data.get("amenities")
                    for amenity_pk in amenities:
                        amenity = Amenity.objects.get(pk=amenity_pk)
                        room.amenities.add(amenity)
                    response_serializer = RoomDetailSerializer(room)
                    # 데이터 생성 성공 시 201 Created
                    return Response(response_serializer.data, status=status.HTTP_200_OK)
            except Exception:
                raise ParseError(detail=serializer.errors)
        else:
            # 유효성 검사 실패 시 400 Bad Request
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RoomDetail(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            # NotFound 예외에 detail 인자를 추가하여 커스텀 메시지를 전달합니다.
            raise NotFound(detail="Room not found.")

    def get(self, request, pk):
        room = self.get_object(pk)
        serializer = RoomDetailSerializer(
            room,
            context={"request": request},
        )
        return Response(serializer.data)

    def put(self, request, pk):
        room = self.get_object(pk)

        if room.owner != request.user:
            raise PermissionDenied

    def delete(self, request, pk):
        room = self.get_object(pk)
        if not request.user.is_authenticated:
            raise NotAuthenticated

        if room.owner != request.user:
            raise PermissionDenied
        room.delete()
        return Response(status=status.HTTP_200_OK)


class Amenities(APIView):

    def get(self, request) -> Response:
        all_amenities = Amenity.objects.all()
        serializer = AmenitySerializer(
            all_amenities,
            many=True,
            context={"request": request},
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request) -> Response:
        serializer = AmenitySerializer(
            data=request.data,
            context={"request": request},
        )
        if serializer.is_valid():
            amenity = serializer.save()
            return Response(AmenitySerializer(amenity).data, status=status.HTTP_200_OK)


class AmenityDetail(APIView):
    def get_object(self, pk):
        try:
            return Amenity.objects.get(pk=pk)
        except Amenity.DoesNotExist:
            # 객체를 찾지 못했을 때 404 Not Found
            raise NotFound(detail="Amenity not found")

    def get(self, request, pk):
        amenity = self.get_object(pk)
        serializer = AmenitySerializer(amenity)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        amenity = self.get_object(pk)
        serializer = AmenitySerializer(
            amenity,
            data=request.data,
            partial=True,
        )

        if serializer.is_valid():
            updated_amenity = serializer.save()
            response_serializer = AmenitySerializer(updated_amenity)
            return Response(response_serializer.data, status=status.HTTP_200_OK)

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        amenity = self.get_object(pk)
        amenity.delete()
        # 데이터 삭제 성공 시 내용이 없다는 의미의 204 No Content
        return Response(status=status.HTTP_204_NO_CONTENT)


class RoomReviews(APIView):
    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound(detail=f"Room Not Found with {pk}")

    def get(self, request, pk):

        try:
            page = request.query_params.get("page", 1)
            page = int(page)
        except ValueError:
            page = 1
        page_size = 3
        start = (page - 1) * page_size
        end = start + page_size
        room = self.get_object(pk)
        serializer = ReviewSerializer(
            room.reviews.all()[start:end],
            many=True,
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


class RoomBookings(APIView):
    """
    API view to retrieve future bookings for a specific room.
    Accessible by any user (read-only), but booking modifications would require authentication.
    """

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, pk):
        """
        Handles GET requests to list future bookings for a room identified by its primary key (pk).

        Returns a list of bookings where the check-in date is after the current date.
        """
        # Retrieve the Room instance using its primary key.
        # If the room does not exist, it will automatically raise an Http404 exception,
        # which DRF translates into a "404 Not Found" response.
        room = get_object_or_404(Room, pk=pk)

        # Get the current date in the local timezone to ensure accurate comparison.
        # We only need the date part, not the time, for filtering bookings.
        today = timezone.localtime(timezone.now()).date()

        # Filter the bookings based on several criteria:
        # 1. The booking must be for the specified room.
        # 2. The booking 'kind' must be 'room' (not 'experience', for example).
        # 3. The check-in date must be in the future (greater than today).
        future_bookings = Booking.objects.filter(
            room=room,
            kind=Booking.BookingKindChoices.ROOM,
            check_in__gt=today,
        )

        # Serialize the list of booking objects into a JSON-representable format.
        # 'many=True' is required because we are serializing a queryset (a list of objects).
        serializer = PublicBookingSerializer(
            future_bookings,
            many=True,
        )

        # Return the serialized data with a "200 OK" status code.
        return Response(serializer.data)

    def post(self, request, pk):
        # Retrieve the room for which the booking is being made.
        # get_object (or get_object_or_404) will handle the "Not Found" case.
        room = self.get_object(pk)

        # Instantiate the serializer with the data from the request payload.
        serializer = CreateRoomBookingSerializer(data=request.data)

        # Validate the incoming data. If validation fails,
        # it raises a ValidationError, and DRF's exception handler
        # will automatically return a 400 Bad Request response with the error details.
        serializer.is_valid(raise_exception=True)

        # If the data is valid, proceed to save the new booking object.
        # We must pass the 'room' and 'user' objects to the save() method,
        # as they are not part of the client's request data but are required
        # to create the Booking model instance.
        booking = serializer.save(
            room=room,
            user=request.user,
            kind=Booking.BookingKindChoices.ROOM,
        )

        # For the response, it's good practice to serialize the newly created object
        # to show the user the result of their action. Here we can reuse the
        # PublicBookingSerializer to show the created booking's public data.
        response_serializer = PublicBookingSerializer(booking)

        # Return the data of the newly created booking along with a
        # '201 Created' HTTP status code, which is the standard for successful creation.
        return Response(
            response_serializer.data,
            status=status.HTTP_201_CREATED,
        )
