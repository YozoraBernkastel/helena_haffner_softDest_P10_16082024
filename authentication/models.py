from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models
from django.utils import timezone


class User(AbstractUser, PermissionsMixin):
    birthday_date = models.DateField()
    can_contact = models.BooleanField(default=False)
    share_personal_data = models.BooleanField(default=False)
    # date_joined = date et heure de création de l'objet
    # last_join (?) = dernière connexion

    REQUIRED_FIELDS = ['password', "birthday_date", "can_contact", "share_personal_data"]

    @property
    def minimal_consent_age(self) -> bool:
        limit_age: int = 15
        fuzzing: int = 0
        today = timezone.now().date()

        if (today.month > self.birthday_date.month
                or (today.month == self.birthday_date.month
                    and today.day > self.birthday_date.day)):
            fuzzing = 1

        return int(today.year - self.birthday_date.year) - fuzzing > limit_age

    def save(self, *args, **kwargs):
        if not self.minimal_consent_age:
            self.can_contact = False
            self.share_personal_data = False

        return super().save(*args, **kwargs)
# todo mettre en place une demande de la date de naissance lorsqu'on crée un superuser via le terminal !!!

