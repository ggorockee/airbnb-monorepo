from django.db import models

from common.models import CommonModel


class Photo(CommonModel):
    file = models.CharField(max_length=150)

    description = models.CharField(
        max_length=140,
    )

    room = models.ForeignKey(
        "room.Room",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="photos",
    )

    experience = models.ForeignKey(
        "experience.Experience",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="photos",
    )

    def __str__(self):
        return "Photo File"


class Video(CommonModel):

    file = models.CharField(max_length=180)

    experience = models.OneToOneField(
        "experience.Experience",
        on_delete=models.CASCADE,
        related_name="videos",
    )

    def __str__(self):
        return "Video File"
