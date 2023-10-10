import pandas as pd
import datetime
import json
import dataframe_image as dfi
import csv


def extract_next_week_schedule(promotion):

    if promotion == "M2S3 23-24":
        old_schedule = pd.read_csv("csv/M2.csv")
    else:
        old_schedule = pd.read_csv("csv/M1.csv")

    with open("/home/ubuntu/deployed_project/scraper_owncloud_geomatique/json/credentials.json", "r") as json_file:
        data = json.load(json_file)
        file_path = data["file_path"]

    df = pd.read_excel(file_path,
                       skiprows=2, sheet_name=promotion)

    today = datetime.date.today()
    days_until_next_monday = (7 - today.weekday()) % 7

    next_monday = today + datetime.timedelta(days=days_until_next_monday)
    next_wensday = next_monday + datetime.timedelta(days=2)

    next_week = df[(df["date"] >= next_monday.strftime('%Y-%m-%d'))
                   & (df["date"] <= next_wensday.strftime('%Y-%m-%d'))]

    # Is there classes next wensday ? Used to state it in an email
    classes_next_wensday = next_week["jour"].str.contains(
        "mercredi").any()

    next_week = next_week.reset_index(drop=True)

    # style the df and export as image
    if promotion == "M1S1 23-24":
        # check if the schedule changed since last time
        schedule_unchanged = old_schedule[["08h30 - 10h30", "10h30 - 12h30", "14h - 16h", "16h-18h"]].equals(
            next_week[["08h30 - 10h30", "10h30 - 12h30", "14h - 16h", "16h-18h"]])
        next_week.to_csv("csv/M1.csv")
        next_week = dfi.export(
            next_week, "M1.png")

    elif promotion == "M2S3 23-24":
        # check if the schedule changed since last time
        schedule_unchanged = old_schedule[["8h30 - 10h30", "10h30 - 12h30", "14h - 16h", "16h-18h"]].equals(
            next_week[["8h30 - 10h30", "10h30 - 12h30", "14h - 16h", "16h-18h"]])
        next_week.to_csv("csv/M2.csv")
        next_week = dfi.export(
            next_week, "M2.png")

    return [classes_next_wensday, schedule_unchanged]
