# About
Welcome to my application for amateur races.
Idea behid this project:
I've seen an amateur race where results were tracked totally analogue. And I've decided it wolud be good to create simple tool that may help to record results and give winner name right after end of race.

It was motorcycle race and the winner was the one who finished biggest number of laps and crossed finish line first.

Most important for me was to create tool to record race number of racer who is passing finish line and after race calculate who won.
When I started to develop this application I decided it would be good and quite easy to implement multiple users and possibility to register multiple races. And as I thought users and races was easiest part. Most of work took preparation of solution to record race number and time of passing finish line. I foud in the internet virtual pin pad created in java script. It was really good for start but also needed many chages to suit my needs.
I had to change behaviour after fetch was succeded. Add creation of timestamp when first digit of race number was entered. And as I wanted it to be device independent i needed to add possibility to use physical keyboard to enter number quicker when using laptop or so.
To not gather unneccessary personal data user may register race attendee who is not allplication user by reservation of race number only.
So I believe it's enough distinctiveness form course projects as it begins as real life problem solution and use of multiple database queries and virtual numpad created in JS make it quite complex.

# What have I done:
+ Registered new app in capstone/settings.py and capstone/urls.py
+ To not inventing wheel again and focus on my part of code I reused register, login, logout from project "network". Also used html files: layout, login and register
+ created following files
+ [urls.py] - as usual urls for all application needs
+ [models.py] - contains all models
    + _User_ - extends AbstractUser with "favourite_race_number" and "info" where users may enter information about themeself
    + _Race_ - information about race: Name, Date and Time, and list of race admins
    + _RaceAttendees_ - for registering race attendee with race number; after race contains also racer results
    + _TemporaryResult_ - for registering race number and time of user passing finish line
    + _RaceAdmin_ - connects Races with Users who have rights to edit Race data and record results
+ [admin.py] - to register models for web access
+ [views.py] - contains all backend functions:
    + _index_ - returns index page with lists of races upcoming and finished
    + _race_ - when POST - records race info to database; when GET returns page with information about race, race attendees and allows admin to modify race data and link to result recording page
    + _user_ - returns page with user info and list of races to which user is registered
    + _admin_ - adds user to race admin list
    + _race_attendee_ - when POST adds user to race attendees list; when DELETE removes attendee from list
    + _temoprary_result_ - records race number and time to database
    + _export_result_ - calculates number of laps and time of finishing last lap and saves it in _RaceAttendees_ table
+ [static/amracing.js] - file which contains all JS for the project except numpad. at the beginning checks html and creates all neccessary buttons, then there are functions defined:
    + _race_ - sends raceinfo to the server
    + _admin_ - sends new admin name to the server
    + _modify_info_ - sends modified user info to the server
    + _race_attendee_ - sends new attendee race number to the server
    + _del_number_ - sends to the server race number to be deleted form race attendees list
    + _visibility_change_ and _about_visibility_change_ - changes visibility of page elements
+ [static/keyboard/keyboard.js] - cpntains functions needed to handle virtual numpad
    + _class NumKeyboard_ - class to create numpad
    + __generatePad_ - generates HTML elements to display numpad
    + __handleKeyboard_ - takes care of physical keyboard input
    + __handleKeyPress_ - takes care of virtual keyboard input
    + __recordTime_ - sends racenumber and timestamp to the server
+ [static/keyboard/keyboard.css] - defines numpad aperance and reactions for correct and incorrect input
+ [templates/amracing] - HTML templates
    + [index] - list of all races in application
    + [race] - race information, results and admin controll buttons
    + [user] - user information and list of races one is registered for
    + [record] - only numpad to enter racenumber (admin only)
    + [race_results] - list of temporary results and button for exporting them to RaceAttendee table (admin only)

# To run application
You just have to start Django server using
```
$python manage.py runserver
```





