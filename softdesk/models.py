from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
from django.db import models


class Project(models.Model):
    creator = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="projects")
    description = models.TextField(max_length=2048, blank=True, verbose_name="description")
    name = models.CharField(max_length=128, verbose_name="nom")
    # todo associer un chiffre à un statut dans le formulaire puis créer une comboBox contenant ces noms de statut!!!!
    #  Utiliser un chiffre pour le statut devrait permettre de prendre moins de place dans la bdd je suppose.
    type = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(4)], verbose_name="type")
    # todo associer un chiffre à un statut dans le formulaire puis créer une comboBox contenant ces noms de statut!!!!
    #  Utiliser un chiffre pour le statut devrait permettre de prendre moins de place dans la bdd je suppose.
    status = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)], verbose_name="statut")
    time_created = models.DateTimeField(auto_now_add=True)
    modification_time = models.DateTimeField(auto_now_add=True)


class Contributor(models.Model):
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="contributors")
    project = models.ForeignKey(
        to=Project, on_delete=models.CASCADE, related_name="contributors")
    time_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        # ensures we don't get multiple UserFollows instances
        # for unique user-user_followed pairs
        unique_together = ('user', 'project',)


class Issue(models.Model):
    creator = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="issues")
    project = models.ForeignKey(
        to=Project, on_delete=models.CASCADE, related_name="issues")
    assigned_user = models.ForeignKey(
        to=Contributor, on_delete=models.CASCADE, related_name="issues")
    # todo associer un chiffre à un statut dans le formulaire puis créer une comboBox contenant ces noms de statut!!!!
    #  Utiliser un chiffre pour le statut devrait permettre de prendre moins de place dans la bdd je suppose.
    status = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)], verbose_name="statut")
    # todo associer un chiffre à un statut dans le formulaire puis créer une comboBox contenant ces noms de statut!!!!
    #  Utiliser un chiffre pour le statut devrait permettre de prendre moins de place dans la bdd je suppose.
    type = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(3)], verbose_name="type")
    # todo associer un chiffre à un statut dans le formulaire puis créer une comboBox contenant ces noms de statut!!!!
    #  Utiliser un chiffre pour le statut devrait permettre de prendre moins de place dans la bdd je suppose.
    priority = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(3)], verbose_name="priorité")
    title = models.CharField(max_length=128, verbose_name="titre")
    description = models.TextField(max_length=2048, blank=True, verbose_name="description")
    time_created = models.DateTimeField(auto_now_add=True)
    modification_time = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    creator = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="comments")
    related_issue = models.ForeignKey(to=Issue, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField(max_length=2048, blank=True, verbose_name="contenu")
    time_created = models.DateTimeField(auto_now_add=True)
    modification_time = models.DateTimeField(auto_now_add=True)
