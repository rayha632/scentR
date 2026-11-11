from django.db import models


# Create your models here.
class Perfume(models.Model):
    id = models.CharField(max_length=255, primary_key=True)

    name = models.CharField(max_length=255)
    house = models.CharField(max_length=255)

    family = models.CharField(max_length=100, blank=True)
    secondary_family = models.CharField(max_length=100, blank=True)

    notes = models.JSONField(default=list)
    top_notes = models.JSONField(default=list)
    heart_notes = models.JSONField(default=list)
    base_notes = models.JSONField(default=list)

    character = models.JSONField(default=list)
    seasons = models.JSONField(default=list)
    times_of_day = models.JSONField(default=list)

    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.house} - {self.name}"
