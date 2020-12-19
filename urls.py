
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile/<str:name>", views.profile, name="profile"),
    path("follow/<str:name>/<str:mod>", views.follow, name="follow"),
    path("like/<int:post_id>/<str:mod>", views.like, name="like"),
    path("post", views.post, name="create_post"),
    path("posts/<str:param>", views.index, name="posts_filtered")
]
