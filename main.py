import send_email
import process_schedule
import datetime
import json
import locale
import scraper


# extract todays day in french
locale.setlocale(locale.LC_TIME, 'fr_FR')
today = datetime.date.today().strftime("%A")


scraper.get_schedule()
classes_next_wensday = process_schedule.extract_next_week_schedule()


with open("json/users.json", "r") as users_file:
    user_data = json.load(users_file)
    for user in user_data:
        if user_data[user] == today:
            send_email.send_email_to_user(
                user, classes_next_wensday)
