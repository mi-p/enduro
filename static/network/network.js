document.addEventListener('DOMContentLoaded', function() {
    if (document.getElementById('post-input')) {
        var form = document.getElementById('post-input');
        form.addEventListener('submit', function(){submit_post("new");});
    };
  });

function follow_change(name, mod) {
    fetch(`../follow/${name}/${mod}`)
    .then(function(data) {
        data.text().then(function(text) {
            console.log(text,"  ",mod);
            document.getElementById("fr_number").innerHTML=text;
            if (mod=="add") {
                document.getElementById("btn_follow").innerHTML = "Unfollow";
                document.getElementById("btn_follow").setAttribute("onclick",`follow_change(name="${name}", mod="del")`);
            } else if (mod == "del") {
                document.getElementById("btn_follow").innerHTML = "Follow";
                document.getElementById("btn_follow").setAttribute("onclick",`follow_change(name="${name}", mod="add")`);
            }
        });
    });
}

function like_change(post_id, mod) {
    fetch(`../like/${post_id}/${mod}`)
    .then(function(data) {
        data.text().then(function(text) {
            document.getElementById(`lc${post_id}`).innerHTML=text;
            if (mod=="add") {
                document.getElementById(`lb${post_id}`).innerHTML = "Unlike";
                document.getElementById(`lb${post_id}`).setAttribute("onclick",`like_change(post_id="${post_id}", mod="del")`);
            } else if (mod == "del") {
                document.getElementById(`lb${post_id}`).innerHTML = "Like";
                document.getElementById(`lb${post_id}`).setAttribute("onclick",`like_change(post_id="${post_id}", mod="add")`);
            }
        });
    });
}

function submit_post(mod) {
    event.preventDefault();
    if (mod == "new") {
        content = document.getElementById('post-content').value
        postId = "x"
    } else if (mod == "ed") {
        content = document.getElementById('post-content-ed').value
        postId = document.getElementById('form-post-id').value
    }

    fetch('/post', {
        method: 'POST',
        body: JSON.stringify({
        content: content,
        id: postId,
        })
    }).then(response => {
        if (response.status == 201) {
            window.location.reload();
            document.getElementById('post-content').value = "";
        } else {
            response.text().then(text => {
                alert(JSON.parse(text).error)
            }) 
        }
    });
}

function edit_post(id) {
    elem = document.getElementById(`post-${id}`)
    post = elem.innerHTML
    csrf = document.querySelector('[name=csrfmiddlewaretoken]').value;
    elem.innerHTML = `<form id="edit-post" class="form-group"><input type="hidden" name="csrfmiddlewaretoken" value="${csrf}"> <textarea class="form-control" id="post-content-ed">${post}</textarea><input type="hidden" id="form-post-id" value="${id}"/><input type="submit" id="edit-submit" class="btn btn-primary" value="Send"/></form>`;
    var form = document.getElementById('edit-post');
    form.addEventListener('submit', function(){submit_post("ed");});
}