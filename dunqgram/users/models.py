from django.contrib.auth.models import AbstractUser
# from django.db.models import CharField
from django.db import models
from django.urls import reverse
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _


class User(AbstractUser):

    """ User Model """

    GENDER_CHOICES = (
        ('mele', 'Mele'),
        ('female', 'Female'),
        ('not-specified', 'Not specified')
    )
    # First Name and Last Name do not cover name patterns
    # around the globe.

    profile_image = models.ImageField(null=True)
    name = models.CharField(_("Name of User"), blank=True, max_length=255)
    website = models.URLField(null=True)
    bio = models.TextField(null=True)
    phone = models.CharField(null=True, max_length=140)
    gender = models.CharField(null=True, max_length=80, choices=GENDER_CHOICES)
    followers = models.ManyToManyField("self", blank=True)
    following = models.ManyToManyField("self", blank=True)

    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"username": self.username})
