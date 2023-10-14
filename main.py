import send_email
import process_schedule
import datetime
import json
import locale
import scraper
import pandas as pd


locale.setlocale(locale.LC_TIME, 'fr_FR')
today = datetime.date.today().strftime("%A")

scraper.get_schedule()
send_email.get_all_emails()


classes_next_wensday_M1, same_schedule_M1 = process_schedule.extract_next_week_schedule(
    "M1S1 23-24")
classes_next_wensday_M2, same_schedule_M2 = process_schedule.extract_next_week_schedule(
    "M2S3 23-24")


def send_email_to_all_users():
    with open("/home/ubuntu/deployed_project/scraper_owncloud_geomatique/json/users.json", "r") as users_file:
        user_data = json.load(users_file)
        for user in user_data:
            if user_data[user] == "M1":
                # to prevent the schedule will be detected as "changed" every sunday
                if today == "dimanche":
                    send_email.send_email_to_user(
                        user, "M1", classes_next_wensday_M1, True)
                else:
                    send_email.send_email_to_user(
                        user, "M1", classes_next_wensday_M1, same_schedule_M1)
            elif user_data[user] == "M2":
                # to prevent the schedule will be detected as "changed" every sunday
                if today == "dimanche":
                    send_email.send_email_to_user(
                        user, "M2", classes_next_wensday_M2, True)
                else:
                    send_email.send_email_to_user(
                        user, "M2", classes_next_wensday_M2, same_schedule_M2)


if same_schedule_M1 == False:
    print("schedule changed M1")
    send_email_to_all_users()
if same_schedule_M2 == False:
    print("schedule changed M2")
    send_email_to_all_users()

if same_schedule_M1 == True & same_schedule_M2 == True:
    print("no changes to schedule")

if today == "dimanche":
    send_email_to_all_users()
