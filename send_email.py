import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import imaplib
import email
from email.header import decode_header
import json
import re
import os

with open("/home/ubuntu/deployed_project/scraper_owncloud_geomatique/json/credentials.json", "r") as json_file:
    data = json.load(json_file)
    sender_email = data["sender_email"]
    sender_password = data["google_key"]


def send_email_to_user(destination_email, promotion, classes_next_wensday, same_schedule):

    # Create the email content
    subject = "Emploi du temps"
    message = "Emploi du temps de la semaine prochaine, contient peut etre des erreurs."
    if classes_next_wensday == False:
        subject += " / Pas cours mercredi"

    if same_schedule == False:
        subject += " - MODIFIE"
        message += " \nL'emploi du temps a peut etre été modifié, si ce n'est pas le cas merci de me le dire <3"

    # Create a MIMEText object for the email  content
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = destination_email
    msg['Subject'] = subject

    # Attach the message to the email

    msg.attach(MIMEText(message, 'plain'))

    # Attach the image as an attachment
    if promotion == "M1":
        with open("/home/ubuntu/deployed_project/scraper_owncloud_geomatique/M1.png", 'rb') as image_file:
            image = MIMEImage(image_file.read(), name='EDT.png')
        msg.attach(image)
    elif promotion == "M2":
        with open("/home/ubuntu/deployed_project/scraper_owncloud_geomatique/M2.png", 'rb') as image_file:
            image = MIMEImage(image_file.read(), name='EDT.png')
        msg.attach(image)

    # Connect to the SMTP server and send the email
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, destination_email, msg.as_string())
        server.quit()
        print("Email sent successfully to : ", destination_email)
    except Exception as e:
        print("An error occurred:", str(e))


def get_all_emails():

    imap_server = "imap.gmail.com"
    imap_port = 993

    # Create an IMAP4 class with SSL
    mail = imaplib.IMAP4_SSL(imap_server, imap_port)

    # Login to account
    mail.login(sender_email, sender_password)

    # Select the mailbox you want to access (e.g., "inbox")
    mailbox = "inbox"
    mail.select(mailbox)

    # Search for all emails in the selected mailbox
    status, email_ids = mail.search(None, "ALL")

    # Fetch the email content for each email
    email_ids = email_ids[0].split()
    with open("/home/ubuntu/deployed_project/scraper_owncloud_geomatique/json/users.json", "r") as users_file:
        user_data = json.load(users_file)

        for email_id in email_ids:
            status, msg_data = mail.fetch(email_id, "(RFC822)")
            msg = email.message_from_bytes(msg_data[0][1])

            # Decode the email subject and sender
            subject, _ = decode_header(msg["Subject"])[0]
            from_field = msg["From"]
            # get only email adress, handle case of annoying poeple with accents in their name
            sender = re.search(
                r'<([^>]+)>', from_field).group(1) if "<" in from_field else from_field

            text_content = ""
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    text_content += part.get_payload(
                        decode=True).decode("utf-8")

            # set value if email sent properly. Will define the day when the email will be send
            if ("M1" in text_content) & (subject.lower() == "subscribe"):
                user_data[sender] = "M1"
            elif ("M2" in text_content) & (subject.lower() == "subscribe"):
                user_data[sender] = "M2"

            # manage unsubscription from email list
            if subject.strip().lower() == "unsubscribe":
                user_data[sender] = ""

    # Logout from the server
    mail.logout()

    # update data
    with open("/home/ubuntu/deployed_project/scraper_owncloud_geomatique/json/users.json", "w") as users_file:
        json.dump(user_data, users_file)
