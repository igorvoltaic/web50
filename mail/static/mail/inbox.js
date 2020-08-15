document.addEventListener('DOMContentLoaded', function() {

    // Use buttons to toggle between views
    document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
    document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
    document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
    document.querySelector('#compose').addEventListener('click', compose_email);
    document.querySelector('#compose-form').onsubmit = sendmail;

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

function read_email(id) {
    document.querySelector('#emails-view').style.display = 'none';
    document.querySelector('#compose-view').style.display = 'none';
    document.querySelector('#reader-view').style.display = 'block';

    fetch(`/emails/${id}`)
    .then(response => response.json())
    .then(email => {
        // Reply an email
        document.querySelector('#reply').addEventListener('click', () => { 
            compose_email();
            let body = ''
            email['body'].split('\n').forEach(line => {body += (`> ${line}\n`)});
            document.querySelector('#compose-recipients').value = `${email['sender']}`;
            document.querySelector('#compose-subject').value = `Re: ${email['subject']}`;
            document.querySelector('#compose-body').value = `On ${email['timestamp']} ${email['sender']} wrote:\n${body}`;
        });
        // Show email
        document.querySelector('#reader-sender').innerHTML = `<b>From:</b> ${email['sender']}`;
        document.querySelector('#reader-recipients').innerHTML = `<b>To:</b> ${email['recipients']}`;
        document.querySelector('#reader-subject').innerHTML = `<b>Subject:</b> ${email['subject']}`;
        document.querySelector('#reader-timestamp').innerHTML = `<b>Timestamp:</b> ${email['timestamp']}`;
        document.querySelector('#reader-body').innerHTML = email['body'].replaceAll('\n', '<br>');
    });
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
            element.className = 'shadow p-2 mb-1 read rounded border container hide';
            const row = document.createElement('div')
            row.className = 'row';
            element.append(row)
            const col = document.createElement('div')
            col.className = 'col-10';
            row.append(col)
            col.innerHTML = `${emails['sender']}  ::  ${emails['subject']}  ::  ${emails['timestamp']}`;
            col.addEventListener('click', function() {
                if (!emails['read']) {
                    // Mark clicked email as read
                    mark_read(emails['id'])
                    element.className = 'shadow p-2 mb-1 read border rounded';
                }
                read_email(emails['id']);
            });
            if (mailbox === 'inbox' || mailbox === 'archive') {
                const button = document.createElement('button');
                button.className = 'ml-5 btn btn-sm btn-outline-primary'
                button.id = 'archive'
                if (emails['archived']) {
                    button.innerHTML = 'Unarchive';
                } else {
                    button.innerHTML = 'Archive';
                }
                button.addEventListener('click', function() {
                    event.preventDefault()
                    if (!emails['archived']) {
                        archive_mail(emails['id'], true);
                    } else {
                        archive_mail(emails['id'], false);
                    }
                    element.style.animationPlayState = 'running';
                    element.addEventListener('animationend', () => {
                        element.remove();
                        load_mailbox('inbox');
                    })
                });
                row.append(button)
            }
            if (!emails['read']) {
                element.className = 'shadow p-2 mb-1 rounded unread';
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

function mark_read(email_id) {
    fetch(`/emails/${email_id}`, {
        method: 'PUT',
        body: JSON.stringify({
            read: true
        })
    })
}

function archive_mail(email_id, state) {
    fetch(`/emails/${email_id}`, {
        method: 'PUT',
        body: JSON.stringify({
            archived: state
        })
    })
}
