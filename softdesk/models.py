from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy


class Project(models.Model):
    BACKEND = "Back-end"
    FRONTEND = "Front-end"
    IOS = "Ios"
    ANDROID = "Androïd"

    TYPE_CHOICES = {
        BACKEND: gettext_lazy("Back-end"),
        FRONTEND: "Front-end",
        IOS: "Ios",
        ANDROID: "Androïd"
    }

    author = models.ForeignKey(
        to="softdesk.Contributor", on_delete=models.CASCADE, related_name="projects")
    description = models.TextField(max_length=2048, blank=True, verbose_name=gettext_lazy("description"))
    name = models.CharField(max_length=128, verbose_name="nom")
    type = models.CharField(max_length=128, choices=TYPE_CHOICES)
    time_created = models.DateTimeField(auto_now_add=True)
    modification_time = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-time_created",)


class Contributor(models.Model):
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name="contributors", null=True)
    project = models.ForeignKey(
        to=Project, on_delete=models.CASCADE, related_name="contributors", null=True)
    time_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'project',)
        ordering = ("-time_created",)


class Issue(models.Model):
    TODO = "ToDo"
    IN_PROGRESS = "In Progress"
    DONE = "Done"
    TO_DISCUSS = "To Discuss"
    CANCELED = "Canceled"

    STATUS_CHOICES = {
        TODO: "ToDo",
        IN_PROGRESS: "In Progress",
        DONE: "Done",
        TO_DISCUSS: "To Discuss",
        CANCELED: "Canceled"
    }

    BUG = "Bug"
    FEATURE = "Feature"
    TASK = "Task"

    TYPE_CHOICES = {
        BUG: "Bug",
        FEATURE: "Feature",
        TASK: "Task"
    }

    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"

    PRIORITY_CHOICES = {
        LOW: "Low",
        MEDIUM: "Medium",
        HIGH: "High"
    }

    author = models.ForeignKey(
        to=Contributor, on_delete=models.CASCADE, related_name="author_issues")
    project = models.ForeignKey(
        to=Project, on_delete=models.CASCADE, related_name="issues")
    assigned_user = models.ForeignKey(
        to=Contributor, on_delete=models.CASCADE, related_name="issues")
    status = models.CharField(max_length=128, choices=STATUS_CHOICES)
    type = models.CharField(max_length=128, choices=TYPE_CHOICES)
    priority = models.CharField(max_length=128, choices=PRIORITY_CHOICES)
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
