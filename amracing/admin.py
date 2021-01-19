from django.contrib import admin

# Register your models here.
#admin.site.register(django_migrations)

from .models import User, Race, RaceAttendees, TemporaryResult

admin.site.register(User)
admin.site.register(Race)
admin.site.register(RaceAttendees)
admin.site.register(TemporaryResult)