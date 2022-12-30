from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse

from sgz.utils.models import SGZModel
from sgz.utils.validators import alphabetic_validator


class User(SGZModel, AbstractUser):
    full_name = models.CharField(
        max_length=50, validators=[alphabetic_validator], help_text="User's full name."
    )
    is_owner = models.BooleanField(
        default=False, help_text="Whether this is an owner user."
    )

    REQUIRED_FIELDS = ["full_name", "is_owner"]

    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"username": self.username})
