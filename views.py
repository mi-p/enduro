from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse

from datetime import datetime
import json
from .models import User, Post, Follow, Like
from django.views.decorators.csrf import csrf_exempt

#for pagination
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.contrib.auth.decorators import login_required

def index(request,param=""):
    User= get_user_model()
    # param = "follow"
    if param  == "":
        posts = Post.objects.all().order_by('-time_stamp')
    elif param == "follow":
        id_list = Follow.objects.values_list('followed', flat="true").filter(follower = request.user)
        followed_list = []
        for user in id_list:
            followed_list.append(User.objects.get(id=user))
        posts = Post.objects.filter(author__in = followed_list).order_by('-time_stamp')
    
    if not request.user.is_anonymous:
        for post in posts:
            if Like.objects.filter(user=request.user,post=post).exists():
                post.mod = "del"
                post.lb = "Unlike"
            else:
                post.mod = "add"
                post.lb = "Like"

    #pagination
    page = request.GET.get("page",1)
    paginator = Paginator(posts, 10)

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return render(request, "network/index.html", {
        "posts":posts
    })

@csrf_exempt
def post(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    auth = User.objects.get(id=request.user.id)
    pid = json.loads(request.body)['id']
    if pid == "x":
        p = Post(
            author = auth,
            content = json.loads(request.body)['content'],
            time_stamp = datetime.now()
        )
    else:
        p=Post.objects.get(id = pid)
        if auth != p.author:
            return HttpResponse({"Youre trying to edit someones else post"}, status=403)
        p.content = json.loads(request.body)['content']
    p.save()
    return HttpResponse({"message": "Post stored successfully."}, status=201)

def like(request,post_id,mod):
    post = Post.objects.get(id=post_id)
    user = User.objects.get(id=request.user.id)
    if mod == "add":
        if Like.objects.filter(user=user,post=post).exists():
            pass
        else:
            post.likes_counter = post.likes_counter +1
            post.save()
            Like(user=user,post=post).save()
    if mod == "del":
        if Like.objects.filter(user=user,post=post).exists():
            post.likes_counter = post.likes_counter -1
            post.save()
            Like.objects.filter(user=user,post=post).delete()
    return HttpResponse(post.likes_counter)
    
def follow(request,name,mod): # przycisk follow/unfollow tylko w profilu
    fd = User.objects.get(username=name)
    fr = User.objects.get(id=request.user.id)
    if mod == "add":
        if Follow.objects.filter(followed=fd,follower=fr).exists():
            pass
        else:
            fd.number_of_followers = fd.number_of_followers +1
            fr.number_of_followed = fr.number_of_followed +1
            fd.save()
            fr.save()
            Follow(followed=fd,follower=fr).save()
    if mod == "del":
        if Follow.objects.filter(followed=fd,follower=fr).exists():
            # fd = User.objects.get(username=name)
            # fr = User.objects.get(id=request.user.id)
            fd.number_of_followers = fd.number_of_followers -1
            fr.number_of_followed = fr.number_of_followed -1
            fd.save()
            fr.save()
            Follow.objects.filter(followed=fd,follower=fr).delete()
    return HttpResponse(fd.number_of_followers)

@login_required
def profile(request,name):
    auth_profile = User.objects.get(username = name)
    posts = Post.objects.filter(author = auth_profile).order_by('-time_stamp')
    btn_show = request.user.username != name
    #check if user follows profile
    if Follow.objects.filter(followed=auth_profile,follower=request.user).exists():
        btn_value = "Unfollow"
        mod="del"
    else:
        btn_value = "Follow"
        mod="add"
    
    for post in posts:
        if Like.objects.filter(user=request.user,post=post).exists():
            post.mod = "del"
            post.lb = "Unlike"
        else:
            post.mod = "add"
            post.lb = "Like"

    #pagination
    page = request.GET.get("page",1)
    paginator = Paginator(posts, 10)

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return render(request, "network/index.html", {
        "posts":posts,
        "prof":auth_profile,
        "btn_show":btn_show,
        "btn_value":btn_value,
        "mod":mod
    })

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
