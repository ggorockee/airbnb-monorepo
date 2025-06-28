from django.urls import path, re_path
from . import views


urlpatterns = [
    path("", views.Rooms.as_view()),
    path("<int:pk>/", views.RoomDetail.as_view()),
    path("amenitiy/", views.Amenities.as_view()),
    path("amenitiy/<int:pk>/", views.AmenityDetail.as_view()),
    re_path(r"^<int:pk>/booking/?$", views.RoomBookings.as_view()),
]
