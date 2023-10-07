import pandas as pd
import datetime
import json
import dataframe_image as dfi


def extract_next_week_schedule():

    with open("json/credentials.json", "r") as json_file:
        data = json.load(json_file)
        file_path = data["file_path"]

    df = pd.read_excel(file_path,
                       skiprows=2, sheet_name="M2S3 23-24")

    today = datetime.date.today()
    days_until_next_monday = (7 - today.weekday()) % 7

    next_monday = today + datetime.timedelta(days=days_until_next_monday)
    next_wensday = next_monday + datetime.timedelta(days=2)

    next_week = df[(df["date"] >= next_monday.strftime('%Y-%m-%d'))
                   & (df["date"] <= next_wensday.strftime('%Y-%m-%d'))]
    next_week_extraction = next_week.drop(columns=["sem", "Unnamed: 10"])

    # Is there classes next wensday ? Used to state it in an email
    classes_next_wensday = next_week_extraction["jour"].str.contains(
        "mercredi").any()

    formated_extraction = next_week_extraction.to_string(
        index=False, justify='left')

    # style the df and export as image
    next_week_extraction = dfi.export(
        next_week_extraction, "cours_semaine.png")

    return classes_next_wensday
