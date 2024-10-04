from django.conf import settings
from django.db import models


class Project(models.Model):
    BACKEND = 1
    FRONTEND = 2
    IOS = 3
    ANDROID = 4

    TYPE_CHOICES = {
        BACKEND: "Back-end",
        FRONTEND: "Front-end",
        IOS: "Ios",
        ANDROID: "Androïd"
    }

    author = models.ForeignKey(
        to=Contributor, on_delete=models.CASCADE, related_name="projects")
    description = models.TextField(max_length=2048, blank=True, verbose_name="description")
    name = models.CharField(max_length=128, verbose_name="nom")
    type = models.IntegerField(max_length=2, choices=TYPE_CHOICES)
    # # todo associer un chiffre à un statut dans le formulaire puis créer une comboBox contenant ces noms de statut!!!!
    # # Utiliser un chiffre pour le statut devrait permettre de prendre moins de place dans la bdd je suppose.
    # status = models.PositiveSmallIntegerField(
    #     validators=[MinValueValidator(0), MaxValueValidator(5)], verbose_name="statut")
    time_created = models.DateTimeField(auto_now_add=True)
    modification_time = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-time_created",)


class Contributor(models.Model):
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="contributors", null=True)
    project = models.ForeignKey(
        to=Project, on_delete=models.CASCADE, related_name="contributors", null=True)
    time_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'project',)
        ordering = ("-time_created",)


class Issue(models.Model):
    TODO = 1
    IN_PROGRESS = 2
    DONE = 3
    TO_DISCUSS = 4
    CANCELED = 5

    STATUS_CHOICES = {
        TODO: "ToDo",
        IN_PROGRESS: "In Progress",
        DONE: "Done",
        TO_DISCUSS: "To Discuss",
        CANCELED: "Canceled"
    }

    BUG = 1
    FEATURE = 2
    TASK = 3

    TYPE_CHOICES = {
        BUG: "Bug",
        FEATURE: "Feature",
        TASK: "Task"
    }

    LOW = 1
    MEDIUM = 2
    HIGH = 3

    PRIORITY_CHOICES = {
        LOW: "Low",
        MEDIUM: "Medium",
        HIGH: "High"
    }

    author = models.ForeignKey(
        to=Contributor, on_delete=models.CASCADE, related_name="issues")
    project = models.ForeignKey(
        to=Project, on_delete=models.CASCADE, related_name="issues")
    assigned_user = models.ForeignKey(
        to=Contributor, on_delete=models.CASCADE, related_name="issues")
    status = models.IntegerField(max_length=2, choices=STATUS_CHOICES)
    type = models.IntegerField(max_length=2, choices=TYPE_CHOICES)
    priority = models.IntegerField(max_length=2, choices=PRIORITY_CHOICES)
    title = models.CharField(max_length=128, verbose_name="titre")
    description = models.TextField(max_length=2048, blank=True, verbose_name="description")
    time_created = models.DateTimeField(auto_now_add=True)
    modification_time = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-time_created",)


class Comment(models.Model):
    author = models.ForeignKey(
        to=Contributor, on_delete=models.CASCADE, related_name="comments")
    related_issue = models.ForeignKey(to=Issue, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField(max_length=2048, blank=True, verbose_name="contenu")
    time_created = models.DateTimeField(auto_now_add=True)
    modification_time = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-time_created",)
