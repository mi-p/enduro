
var form = document.getElementById('race-form');
if (form){
    race_id = document.getElementById("js-data").dataset.raceId;
    form.addEventListener('submit', function() {race(race_id);},false);
}

var attend = document.getElementById('attend-form');
if (attend) {
    attend.addEventListener('submit', function() {race_attendee(true);},false);
}

var attend_other = document.getElementById('attendee-form');
if (attend_other) {
    attend_other.addEventListener('submit', function() {race_attendee(false);},false);
}

var admin_form = document.getElementById('admin-form');
if (admin_form){
    admin_form.addEventListener('submit', admin);
}

var about_form = document.getElementById('about-form');
if (about_form){
    username = document.getElementById("nav-username").innerHTML;
    info = document.getElementById("user-about-input").value;
    about_form.addEventListener('submit', function() {modify_info(username,info);}, false);
}

function race(race_id) {
    event.preventDefault();
    date = document.getElementById('race-date').value
    time = document.getElementById('race-time').value
    fetch(`/race/${race_id}`, {
        method: 'POST',
        credentials: 'same-origin',
        headers: {"X-CSRFToken": document.querySelector("input[name='csrfmiddlewaretoken']").value},
        body: JSON.stringify({
        name: document.getElementById('race-name').value,
        date: date+" "+time,
        csrfmiddlewaretoken: document.querySelector("input[name='csrfmiddlewaretoken']").value
        })
    }).then(response => {
        if (response.status == 201) {
            window.location.reload();
            document.getElementById('race-name').value = "";
            document.getElementById('race-date').value = "";
            document.getElementById('race-time').value = "";
        } else {
            response.text().then(text => {
                alert(JSON.parse(text).error)
            }) 
        }
    });
}

function admin() {
    event.preventDefault();
    fetch('/admin', {
        method: 'POST',
        headers: {"X-CSRFToken": document.querySelector("input[name='csrfmiddlewaretoken']").value},
        body: JSON.stringify({
        user_name: document.getElementById('admin-name').value,
        race_id: document.getElementById("js-data").dataset.raceId,
        })
    }).then(response => {
        if (response.status == 201) {
            window.location.reload();
            document.getElementById('admin-name').value = "";
        } else {
            response.text().then(text => {
                alert(JSON.parse(text).error)
            }) 
        }
    });
}

function modify_info(user_name,info) {
    event.preventDefault();
    info = document.getElementById("user-about-input").value;
    number = document.getElementById("user-number-input").value;
    fetch(`/profile/${user_name}`, {
        method: 'PATCH',
        headers: {"X-CSRFToken": document.querySelector("input[name='csrfmiddlewaretoken']").value},
        body: JSON.stringify({
        info: info,
        number: number,
        })
    }).then(response => {
        if (response.status == 201) {
        } else {
            response.text().then(text => {
                alert(JSON.parse(text).error)
            }) 
        }
    });
}

function race_attendee(self) {
    event.preventDefault();
    race_id = document.getElementById("js-data").dataset.raceId;
    if (self) {
        race_number=document.getElementById('attendee-self-number').value;
    } else {
        race_number=document.getElementById('attendee-other-number').value;
    };
    fetch('/attendee', {
        method: 'POST',
        headers: {"X-CSRFToken": document.querySelector("input[name='csrfmiddlewaretoken']").value},
        body: JSON.stringify({
        race_id: race_id,
        race_number: race_number,
        self: self,
        })
    }).then(response => {
        if (response.status == 201) {
            window.location.reload();
            document.getElementById('attendee-other-number').value = "";
        } else {
            response.text().then(text => {
                alert(JSON.parse(text).error)
            }) 
        }
    });
}

function del_number(race_number) {
    race_id = document.getElementById("js-data").dataset.raceId;
    fetch('/attendee', {
        method: 'DELETE',
        headers: {"X-CSRFToken": document.querySelector("input[name='csrfmiddlewaretoken']").value},
        body: JSON.stringify({
        race_id: race_id,
        race_number: race_number,
        })
    }).then(response => {
        if (response.status == 201) {
            window.location.reload();
        } else {
            response.text().then(text => {
                alert(JSON.parse(text).error)
            }) 
        }
    });
}

function visibility_change(id){
    form = document.getElementById(id)
    if (form.style.display == "none") {
        form.style.display = "block";
    }
    else {
        form.style.display = "none";
    }
}

function about_visibility_change(){
    form = document.getElementById("user-about");
    btn = document.getElementById("about-button");

    if (form.style.display == "none") {
        form.style.display = "block";
        btn.innerHTML = "&#9650; Hide";
    }
    else {
        form.style.display = "none";
        btn.innerHTML = "&#9660; Show";
    }
}

function set_now(){
    var t = new Date(Date.now());
    document.getElementById('race-date').value = t.getFullYear()+'-'+("0" + (t.getUTCMonth()+1)).slice(-2)+'-'+("0" + t.getUTCDate()).slice(-2);
    document.getElementById('race-time').value = ("0" + t.getUTCHours()).slice(-2) + ":" + ("0" + t.getUTCMinutes()).slice(-2);
}