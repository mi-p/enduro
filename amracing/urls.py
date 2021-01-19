from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("record/<str:race_id>", views.record, name="record"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("race/<str:race_id>", views.race, name="race"),
    path("admin", views.admin, name="admin"),
    path("attendee", views.race_attendee, name="attendees"),
    path("results/<str:race_id>", views.temporary_result, name="temporary_results"),
    path("export/<str:race_id>", views.export_result, name="export"),
    path("profile/<str:username>", views.user, name="profile"),
]