from django.conf import settings
from django.db import models

from common.models import CommonModel


class Wishlist(CommonModel):
    """Wishlist Model Definition"""

    name = models.CharField(
        max_length=150,
    )

    rooms = models.ManyToManyField(
        "room.Room",
        related_name="wishlists",
    )

    experiences = models.ManyToManyField(
        "experience.Experience",
        related_name="wishlists",
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="wishlists",
    )

    def __str__(self) -> str:
        return self.name
