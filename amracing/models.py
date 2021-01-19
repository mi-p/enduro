from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class User(AbstractUser):
    favourite_race_number = models.CharField(max_length=6, blank=True, null=True)
    info = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.username

class Race(models.Model):
    name = models.CharField(max_length=100)
    admin_list = models.ManyToManyField(User, through="RaceAdmin")
    date = models.DateTimeField(blank=True, null=True)


class RaceAttendees(models.Model):
    race = models.ForeignKey(Race, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    race_number = models.CharField(max_length=6)
    result_laps = models.PositiveIntegerField(blank=True, null=True)
    result_time = models.DurationField(blank=True, null=True)

    class Meta:
        unique_together = [['race_id', 'race_number']] # check if unique in race_id range

class TemporaryResult(models.Model):
    race = models.ForeignKey(Race, on_delete=models.CASCADE)
    attendee = models.ForeignKey(RaceAttendees, on_delete=models.CASCADE)
    lap_time = models.DateTimeField()

#table instead of manytomany field for easier controll
class RaceAdmin(models.Model):
    race = models.ForeignKey(Race, on_delete=models.CASCADE)
    admin = models.ForeignKey(User, on_delete=models.CASCADE)
