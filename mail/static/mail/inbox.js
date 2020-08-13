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

    // Clear out composition fields
    document.querySelector('#compose-recipients').value = '';
    document.querySelector('#compose-subject').value = '';
    document.querySelector('#compose-body').value = '';
}

function load_mailbox(mailbox) {
    //fetch emails
    show_mails(mailbox)

    // Show the mailbox and hide other views
    document.querySelector('#emails-view').style.display = 'block';
    document.querySelector('#compose-view').style.display = 'none';

    // Show the mailbox name
    document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

    // Add the current state to the history
    // history.pushState({mailbox: mailbox}, "", `${mailbox}`);
}

function show_mails(name) {
    fetch(`/emails/${name}`)
    .then(response => response.json())
    .then(emails => {

        //Create and append element for each email
        emails.forEach(emails => {
            const element = document.createElement('div');
            element.className = 'emails read';
            element.innerHTML = emails['sender'] + '  :  ' + emails['subject'] + '  :  ' + emails['timestamp'];
            element.addEventListener('click', function() {
                if (!emails['read']) {
                    fetch('/emails/' + emails['id'], {
                        method: 'PUT',
                        body: JSON.stringify({
                            read: true
                        })
                    })
                    element.className = 'emails read';
                }
            });
            if (!emails['read']) {
                element.className = 'emails unread';
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
        // Print result
        console.log(result);
    });
    load_mailbox('sent')

    // Prevent default submission
    return false;
}

