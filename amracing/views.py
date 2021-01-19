from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
import json
from django.db import IntegrityError
from django.db.models import Max
import datetime
import pytz
from .models import User, Race, RaceAttendees, TemporaryResult, RaceAdmin

def index(request):
    finished_ids = RaceAttendees.objects.filter(result_time__isnull = False).values('race_id').distinct()
    races_upcoming = Race.objects.exclude(id__in = finished_ids).distinct().order_by('date')
    races_finished = Race.objects.filter(id__in = finished_ids).distinct().order_by('-date')
    return render(request, 'amracing/index.html', {"races_finished":races_finished, "races_incoming":races_upcoming})

def record(request, race_id):
    results = RaceAttendees.objects.filter(race_id=race_id, result_time__isnull = False).count()
    race_name = Race.objects.filter(id=race_id).values('name')[0]['name']
    return render(request, 'amracing/record.html', {"race_id":race_id, "race_name":race_name, "results":results})


# @csrf_exempt
def race(request, race_id = ""):
    if request.method == "POST":
        # add race
        print ('>csrf>',request.POST.get('csrfmiddlewaretoken'))
        name = json.loads(request.body)['name']
        date = json.loads(request.body)['date']
        if not Race.objects.filter(name=name).exists():
            if race_id == "0":
                race = Race(
                    name = name,
                    date = date,
                )
                race.save()
                user = User.objects.get(id = request.user.id)
                race.admin_list.add(user)
            else:
                race = Race.objects.get(id = race_id)
                race.name = name
                race.date = date
            race.save()
            return JsonResponse({"message": "New race registered"}, status=201)
        else:
            return JsonResponse({
            "error": "We probably have that race"}, status=400)

    if request.method == "GET":
        race = Race.objects.get(id = race_id)
        admin_list = race.admin_list.all()
        if request.user:
            admin = request.user in admin_list
        else:
            admin = False
        finished = RaceAttendees.objects.filter(race_id=race_id).filter(result_time__isnull = False).count()
        if (finished > 0):
            attendees = RaceAttendees.objects.filter(race_id=race_id).exclude(race_number = "000").exclude(result_laps__isnull = True).select_related('user').order_by('-result_laps','result_time')
            for attendee in attendees:
                if isinstance(attendee.result_time, datetime.timedelta):
                    sec = attendee.result_time.seconds
                    attendee.result_time = str(datetime.timedelta(seconds = sec))
        else:
            attendees = RaceAttendees.objects.filter(race_id=race_id).all().select_related('user')
        return render(request, 'amracing/race.html', {"race":race, "admin_list":admin_list, "admin":admin, "attendees":attendees, "finished":finished})

# @csrf_exempt
def user(request, username):
    if request.method == "GET":
        user = User.objects.get(username = username)
        races_incoming = RaceAttendees.objects.filter(user = user.id).filter(result_time__isnull = True).select_related('race').order_by('race__date')
        races_finished = RaceAttendees.objects.filter(user = user.id).filter(result_time__isnull = False).select_related('race').order_by('-race__date')
        return render(request, 'amracing/user.html', {"races_finished":races_finished, "races_incoming":races_incoming, "user":user})

    if request.method == "PATCH":
        user = User.objects.get(username = username)
        user.info = json.loads(request.body)['info']
        user.favourite_race_number = json.loads(request.body)['number']
        user.save()
        return JsonResponse({"message": "Info modified"}, status=201)


# @csrf_exempt
def admin(request):
        if request.method == "POST":
        # add admin
            race_id = json.loads(request.body)['race_id']
            user_name = json.loads(request.body)['user_name']
            if User.objects.filter(username = user_name).exists():
                user = User.objects.get(username = user_name)
            else:
                return JsonResponse({
                "error": "No such username in database"
                }, status=400)
            race = Race.objects.get(id = race_id)
            race.admin_list.add(user)
            race.save()
            return JsonResponse({"message": "New admin added"}, status=201)


# @csrf_exempt
def race_attendee(request):
    if request.method == "POST":
        requestj = json.loads(request.body)
        race = requestj['race_id']
        race_number = requestj['race_number']
        user = ""
        if requestj['self']:
            user = request.user
        if not RaceAttendees.objects.filter(race_id=race, race_number=race_number).exists():
            if user == "":
                attendee = RaceAttendees(
                    race_id = race,
                    race_number = race_number,
                )
            else:
                if not RaceAttendees.objects.filter(race_id=race, user=user).exists():
                    attendee = RaceAttendees(
                        race_id = race,
                        race_number = race_number,
                        user_id = user.id,
                    )
                else:
                    return JsonResponse({"error": "User may register only one number for himself"}, status=400)
            attendee.save()
            return JsonResponse({"message": "Attendee added"}, status=201)
        else:
            return JsonResponse({"error": "We've got that number registered for that race"}, status=400)

    if request.method == "DELETE":
        requestj = json.loads(request.body)
        race = requestj['race_id']
        race_number = requestj['race_number']
        RaceAttendees.objects.filter(race = race, race_number = race_number).delete()
        return JsonResponse({"message": "Race number released"}, status=201)
    

# @csrf_exempt
def temporary_result(request,race_id = ""):
    print (race_id)
    if request.method == "POST":
        # add race
        requestj = json.loads(request.body)
        race = requestj['race_id']
        race_number = requestj['race_number']
        time = requestj['time']
        #Check if user is admin
        if RaceAdmin.objects.filter(race=race, admin=request.user).exists():
            if race_number == "000":
                race = Race.objects.get(id=race)
                race.date = time
                race.save()
                return HttpResponse("started", status=200)
            else:
                if RaceAttendees.objects.filter(race_id = race, race_number=race_number).exists():
                    attendee = RaceAttendees.objects.get(race_id = race, race_number=race_number)
                    temporary_result = TemporaryResult(
                        race_id = race,
                        attendee = attendee,
                        lap_time = time
                    )
                    temporary_result.save()
                    return HttpResponse("added", status=200)
                else:
                    return JsonResponse({"message": "Not existing race number"}, status=403)
        else:
            return JsonResponse({"message": "You aren't admin of this race"}, status=403)

    if request.method == "GET":
        start = Race.objects.filter(id = race_id).values('date')[0]['date']
        results = TemporaryResult.objects.filter(race_id = race_id).select_related('attendee')
        return render(request, 'amracing/race_results.html', {"results":results, "race_id":race_id, "start":start})

def export_result(request,race_id):
    
    class Result:
        def __init__(self, number, laps, time):
            self.number = number
            self.laps = laps
            self.time = time
    start = Race.objects.get(id = race_id).date
    numbers = TemporaryResult.objects.filter(race_id = race_id).select_related('attendee').values('attendee__race_number').distinct()
    for number in numbers:
        res = Result("","","")
        time = TemporaryResult.objects.filter(race_id = race_id).select_related('attendee').filter(attendee__race_number = number['attendee__race_number']).aggregate(Max('lap_time'))['lap_time__max']
        res.number = number['attendee__race_number']
        res.laps = TemporaryResult.objects.filter(race_id = race_id).select_related('attendee').filter(attendee__race_number = number['attendee__race_number']).count()
        res.time = time - start
        attendee = RaceAttendees.objects.filter(race=race_id).get(race_number = res.number)
        attendee.result_time = res.time
        attendee.result_laps = res.laps
        attendee.save()
    
    return redirect("race", race_id = race_id)


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
            return render(request, "amracing/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "amracing/login.html")


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
            return render(request, "amracing/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "amracing/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "amracing/register.html")
