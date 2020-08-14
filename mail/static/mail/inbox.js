document.addEventListener('DOMContentLoaded', function() {

    // Use buttons to toggle between views
    document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
    document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
    document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
    document.querySelector('#compose').addEventListener('click', compose_email);
    document.querySelector('#compose-form').onsubmit = sendmail;
    // document.querySelectorAll('#archive').forEach(button => {button.onclick = archive_email});

    // By default, load the inbox
    load_mailbox('inbox');
});

// window.onpopstate = function(event) {
//     console.log(event.state.mailbox);
//     load_mailbox(event.state.mailbox);
// }

function compose_email() {

    // Show compose view and hide other views
    document.querySelector('#emails-view').style.display = 'none';
    document.querySelector('#compose-view').style.display = 'block';
    document.querySelector('#reader-view').style.display = 'none';

    // Clear out composition fields
    document.querySelector('#compose-recipients').value = '';
    document.querySelector('#compose-subject').value = '';
    document.querySelector('#compose-body').value = '';
}

function read_email(sender, recipients, subject, timestamp, body) {
    document.querySelector('#emails-view').style.display = 'none';
    document.querySelector('#compose-view').style.display = 'none';
    document.querySelector('#reader-view').style.display = 'block';

    // Clear out composition fields
    document.querySelector('#reader-sender').innerHTML = `<b>From:</b> ${sender}`;
    document.querySelector('#reader-recipients').innerHTML = `<b>To:</b> ${recipients}`;
    document.querySelector('#reader-subject').innerHTML = `<b>Subject:</b> ${subject}`;
    document.querySelector('#reader-timestamp').innerHTML = `<b>Timestamp:</b> ${timestamp}`;
    document.querySelector('#reader-body').innerHTML = body;
}

function load_mailbox(mailbox) {

    // Show the mailbox and hide other views
    document.querySelector('#emails-view').style.display = 'block';
    document.querySelector('#compose-view').style.display = 'none';
    document.querySelector('#reader-view').style.display = 'none';

    // Show the mailbox name
    document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

    //fetch emails
    show_mails(mailbox)

    // Add the current state to the history
    // history.pushState({mailbox: mailbox}, "", `${mailbox}`);
}

function show_mails(mailbox) {
    fetch(`/emails/${mailbox}`)
    .then(response => response.json())
    .then(emails => {

        //Create and append element for each email
        emails.forEach(emails => {
            const element = document.createElement('div');
            element.className = 'shadow p-2 mb-1 read rounded border container';
            if (mailbox === 'inbox' || mailbox === 'archive') {
                if (emails['archived']) {
                    element.innerHTML = `<div class="row"><div class="col-10">${emails['sender']}  ::  ${emails['subject']}  ::  ${emails['timestamp']}</div><button class="ml-5 btn btn-sm btn-outline-primary" id="archive">Unarchive</button></div>`;
                } else {
                    element.innerHTML = `<div class="row"><div class="col-10">${emails['sender']}  ::  ${emails['subject']}  ::  ${emails['timestamp']}</div><button class="ml-5 btn btn-sm btn-outline-primary" id="archive">Archive</button></div>`;
                }
            } else {
                element.innerHTML = `<div class="row"><div class="col-10">${emails['sender']}  ::  ${emails['subject']}  ::  ${emails['timestamp']}</div></div>`;
            }
            element.children[0].children[0].addEventListener('click', function() {
                if (!emails['read']) {
                    fetch(`/emails/${emails['id']}`, {
                        method: 'PUT',
                        body: JSON.stringify({
                            read: true
                        })
                    })

                    // Mark clicked email as read
                    element.className = 'shadow p-2 mb-1 read border rounded';
                }
                fetch(`/emails/${emails['id']}`)
                .then(response => response.json())
                .then(email => {

                    // Show clicked email
                    read_email(email['sender'], email['recipients'], email['subject'], email['timestamp'], email['body'])
                });
            });
            if (!emails['read']) {
                element.className = 'shadow p-2 mb-1 rounded unread';
            }
            if (mailbox === 'inbox' || mailbox === 'archive') {
                element.children[0].children[1].addEventListener('click', function() {
                    event.preventDefault()
                    if (!emails['archived']) {
                        fetch(`/emails/${emails['id']}`, {
                            method: 'PUT',
                            body: JSON.stringify({
                                archived: true
                            })
                        })
                        .then(result => {
                            element.style.animationPlayState = 'running';
                            element.addEventListener('animationend', () => {
                                element.remove();
                                load_mailbox('inbox');
                            })
                        });
                    } else {
                        fetch(`/emails/${emails['id']}`, {
                            method: 'PUT',
                            body: JSON.stringify({
                                archived: false
                            })
                        })
                        .then(result => {
                            element.style.animationPlayState = 'running';
                            element.addEventListener('animationend', () => {
                                element.remove();
                                load_mailbox('inbox');
                            })
                        });
                    }
                });
            }
            document.querySelector('#emails-view').append(element);
        });
    });
}

function sendmail() {
    fetch('/emails', {
        method: 'POST',
        body: JSON.stringify({
            recipients: document.querySelector('#compose-recipients').value,
            subject: document.querySelector('#compose-subject').value,
            body: document.querySelector('#compose-body').value
        })
    })
    .then(response => response.json())
    .then(result => {

        // Open Sent mailbox
        load_mailbox('sent')
    });

    // Prevent default submission
    return false;
}

