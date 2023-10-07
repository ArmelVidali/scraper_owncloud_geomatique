import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

with open("credentials.json", "r") as json_file:
    sender_email = json_file["email"]
    sender_password = json_file["email_password"]
    test_email = json_file["test_email"]


# Create the email content
subject = "Hello, World!"
message = "This is a test email sent from Python."

# Create a MIMEText object for the email content
msg = MIMEMultipart()
msg['From'] = sender_email
msg['To'] = test_email
msg['Subject'] = subject

# Attach the message to the email
msg.attach(MIMEText(message, 'plain'))

# Connect to the SMTP server and send the email
try:
    # Using Gmail's SMTP server as an example
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender_email, sender_password)
    server.sendmail(sender_email, test_email, msg.as_string())
    server.quit()
    print("Email sent successfully.")
except Exception as e:
    print("An error occurred:", str(e))
