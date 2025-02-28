from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


# Create your models here.
class Task(models.Model):

    class PriorityChoices(models.TextChoices):
        HIGH = "High", _("High")
        MEDIUM = "Medium", _("Medium")
        LOW = "Low", _("Low")

    title = models.CharField(max_length=150, blank=False, null=False)
    description = models.TextField(blank=True, null=True)
    due_date = models.DateField(auto_now=False, auto_now_add=False)
    priority = models.CharField(
        max_length=10,
        choices=PriorityChoices.choices,
        default=PriorityChoices.MEDIUM,
    )
    is_completed = models.BooleanField(
        default=False,
    )
    added_by = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name=_("Added By"), related_name="tasks"
    )
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["due_date"]

    def __str__(self):
        return f"{self.title} ({self.priority})"
