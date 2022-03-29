import pandas as pd
from datetime import datetime, timedelta

# get start date and end date from schedule data
df_schedule = pd.read_csv("data staging/schedule.csv")
df_schedule = df_schedule[["ID", "START_DT", "END_DT"]].drop_duplicates(keep="first")

# get semester from enrollment data
df_enrollment = pd.read_csv("data source/enrollment.csv")
df_enrollment = df_enrollment[["SCHEDULE_ID", "SEMESTER"]].drop_duplicates(keep="first")

# merge both dataframe into one
df_sch_enr = df_schedule.merge(df_enrollment, left_on="ID", right_on="SCHEDULE_ID", how="inner")
df_sch_enr = df_sch_enr[["START_DT", "END_DT", "SEMESTER"]].drop_duplicates()

# generate week of semester dimension
week_of_semesters = []
for idx, row in df_sch_enr.iterrows():
    start_date = datetime.strptime(row["START_DT"], "%d-%b-%y")
    end_date = datetime.strptime(row["END_DT"], "%d-%b-%y")
    semester = row["SEMESTER"]

    start_week = start_date
    week = 1
    while start_date <= end_date:
        wos = {}
        wos["date"] = start_date.strftime("%Y-%m-%d")
        wos["week"] = week
        wos["semester"] = semester
        # get weekday number with assumption it starts with 2 as Monday and end at 6 as Friday
        wos["weekday"] = start_date.weekday() + 1
        week_of_semesters.append(wos)

        start_date += timedelta(days=1)
        if start_date == start_week + timedelta(days=7):
            start_week = start_date
            week += 1

df_wos = pd.DataFrame(week_of_semesters)
df_wos.index.name = "id"

# store dimension week of semester to data destination table
df_wos.to_csv("data destination/dim_week_of_semester.csv")