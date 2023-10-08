import send_email
import process_schedule
import datetime
import json
import locale
import scraper


scraper.get_schedule()
send_email.get_all_emails()
classes_next_wensday_M1 = process_schedule.extract_next_week_schedule(
    "M1S1 23-24")
classes_next_wensday_M2 = process_schedule.extract_next_week_schedule(
    "M2S3 23-24")


with open("json/users.json", "r") as users_file:
    user_data = json.load(users_file)
    for user in user_data:
        if user_data[user] == "M1":
            send_email.send_email_to_user(
                user, "M1", classes_next_wensday_M1)
        elif user_data[user] == "M2":
            send_email.send_email_to_user(
                user, "M2", classes_next_wensday_M1)
