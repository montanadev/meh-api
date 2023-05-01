from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.utils.translation import gettext_lazy as _


class Member(AbstractUser):
    groups = models.ManyToManyField(
        Group,
        verbose_name=_("groups"),
        blank=True,
        help_text=_(
            "The groups this user belongs to. A user will get all permissions "
            "granted to each of their groups."
        ),
        related_query_name="member",
        related_name="%(app_label)s_%(class)s_related",  # Add this line
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_("user permissions"),
        blank=True,
        help_text=_("Specific permissions for this user."),
        related_query_name="member",
        related_name="%(app_label)s_%(class)s_related",  # Add this line
    )
