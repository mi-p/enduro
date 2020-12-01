document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  var form = document.getElementById('compose-form');
  form.addEventListener('submit', submit_mail);//(event) => {

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#email-display').style.display = 'none';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#email-display').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  fetch(`/emails/${mailbox}`).then(function (response) {
    return response.json();
  }).then(data => {
    data.forEach(mail => {
        document.getElementById('emails-view').innerHTML += `<button id="${mail.id}" class="mail read-${mail.read}" data-mailid="${mail.id}" onclick="show_mail(${mail.id},'${mailbox}')">` + "From: " + mail.sender + '</br> Subject: ' + mail.subject + "</br> On: " + mail.timestamp + '</button></br>';
      });
  })
};

function show_mail(mail_id,source) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#email-display').style.display = 'block';

  // Decide to show buttons based on what inbox
  btnBlck = document.getElementById("button-block");
  if (source=="sent") {
    btnBlck.style.display = 'none';
  }
  else {
    btnBlck.style.display = 'block';
  };

  fetch(`/emails/${mail_id}`).then(function (response) {
    return response.json();
  }).then(mail => {
    document.getElementById('email').innerHTML = `<div id="${mail.id}" class="mail" >` + "From: " + mail.sender + "   On: " + mail.timestamp + "</br> To: " + mail.recipients + '</br> Subject: ' + mail.subject + '</br></br>' + mail.body + '</div></br>';

    // Set correct parameters to button
    aBtn = document.getElementById('arch_btn');
    aBtn.setAttribute("onClick",`archived_change(${mail.archived},${mail.id})`);
    if (mail.archived == false) {
      aBtn.innerHTML  = "Archive";
    } else {
      aBtn.innerHTML  = "Unarchive";
    };
    document.getElementById('reply_btn').addEventListener('click', function() {
      reply(mail)
    });
  })

  fetch(`/emails/${mail_id}`, {
    method: 'PUT',
    body: JSON.stringify({
        read: true
    })
  });
};

function archived_change(arch_state,mail_id) {
  fetch(`/emails/${mail_id}`, {
    method: 'PUT',
    body: JSON.stringify({
        archived: !arch_state
    })
  });
  load_mailbox('inbox');
}

function submit_mail() {
  event.preventDefault();
  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
      recipients: document.getElementById('compose-recipients').value,
      subject: document.getElementById('compose-subject').value,
      body: document.getElementById('compose-body').value,
    })
  }).then(response => {

      if (response.status == 201) {
        load_mailbox('sent');
      } else {
        response.text().then(text => {
          alert(JSON.parse(text).error)
        }) 
      }
  });

}

function reply(mail) {
  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#email-display').style.display = 'none';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = mail.sender;
  if (mail.subject.substring(0,4) == "Re: ") {
    document.querySelector('#compose-subject').value = mail.subject;
  } else {
    document.querySelector('#compose-subject').value = 'Re: ' + mail.subject;
  }
  document.querySelector('#compose-body').value = "On: " + mail.timestamp + ' ' + mail.sender + ' Wrote: \n' + mail.body;
}