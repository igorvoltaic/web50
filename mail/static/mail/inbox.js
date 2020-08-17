document.addEventListener('DOMContentLoaded', function() {

    // Use buttons to toggle between views
    document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
    document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
    document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
    document.querySelector('#compose').addEventListener('click', () => compose_email());
    document.querySelector('#compose-form').onsubmit = sendmail;

    // By default, load the inbox
    load_mailbox('inbox');
});

window.onpopstate = () => {
    if (event.state.mailbox !== 'compose') {
        load_mailbox(event.state.mailbox, event)
    } else {
        compose_email(event)
    }
}


function compose_email(popstate) {

    // Show compose view and hide other views
    document.querySelector('#emails-view').style.display = 'none';
    document.querySelector('#compose-view').style.display = 'block';
    document.querySelector('#reader-view').style.display = 'none';

    // Clear out composition fields
    document.querySelector('#compose-recipients').value = '';
    document.querySelector('#compose-subject').value = '';
    document.querySelector('#compose-body').value = '';

    // If there is no popstate event add the current state to the history
    if (!popstate) {
        history.pushState({mailbox: 'compose'}, '', 'compose');
    }
}


function load_mailbox(mailbox, popstate) {

    // Show the mailbox and hide other views
    document.querySelector('#emails-view').style.display = 'block';
    document.querySelector('#compose-view').style.display = 'none';
    document.querySelector('#reader-view').style.display = 'none';

    // Show the mailbox name
    document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

    // Fetch emails
    show_mails(mailbox)

    // If there is no popstate event add the current state to the history
    if (!popstate) {
        history.pushState({mailbox: mailbox}, '', mailbox);
    }
}


function read_email(id, mailbox) {
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
        // Add archive button
        if (mailbox === 'inbox' || mailbox === 'archive') {
            document.querySelector('#archive').style.display = 'inline-block';
            if (email['archived']) {
                document.querySelector('#archive').innerHTML = 'Unarchive';
            } else {
                document.querySelector('#archive').innerHTML = 'Archive';
            }
        } else {
            document.querySelector('#archive').style.display = 'none';
        }
        document.querySelector('#archive').onclick = () => {
            if (!email['archived']) {
                archive_mail(email['id'], true);
            } else {
                archive_mail(email['id'], false);
            }
        }


        // Show email
        document.querySelector('#reader-sender').innerHTML = `<b>From:</b> ${email['sender']}`;
        document.querySelector('#reader-recipients').innerHTML = `<b>To:</b> ${email['recipients']}`;
        document.querySelector('#reader-subject').innerHTML = `<b>Subject:</b> ${email['subject']}`;
        document.querySelector('#reader-timestamp').innerHTML = `<b>Timestamp:</b> ${email['timestamp']}`;
        document.querySelector('#reader-body').innerHTML = email['body'].replaceAll('\n', '<br>');
    });
}


function show_mails(mailbox) {
    fetch(`/emails/${mailbox}`)
    .then(response => response.json())
    .then(emails => {

        //Create and append element for each email
        emails.forEach(emails => {
            const element = document.createElement('div');
            element.className = 'shadow p-2 mb-1 read rounded border emails';
            element.innerHTML = `${emails['sender']}  ::  ${emails['subject']}  ::  ${emails['timestamp']}`;
            element.addEventListener('click', function() {
                if (!emails['read']) {
                    // Mark clicked email as read
                    mark_read(emails['id'])
                    element.className = 'shadow p-2 mb-1 read border rounded emails';
                }
                read_email(emails['id'], mailbox);
            });
            if (!emails['read']) {
                element.className = 'shadow p-2 mb-1 rounded unread emails';
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
    .then(result => {
        load_mailbox('inbox')
    });
}
