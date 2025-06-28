from django.urls import path
from .views import PerkDetail, Perks

urlpatterns = [
    path("perk/", Perks.as_view()),
    path("perk/<int:pk>/", PerkDetail.as_view()),
]
