import pandas as pd
from datetime import datetime

# merge all involved data
df_enrollment = pd.read_csv("data source/enrollment.csv")
df_enrollment = df_enrollment[["STUDENT_ID", "SCHEDULE_ID", "SEMESTER"]]

df_schedule = pd.read_csv("data staging/schedule.csv")
df_schedule = df_schedule[["ID", "COURSE_ID", "COURSE_DAYS"]]

df_wos = pd.read_csv("data destination/dim_week_of_semester.csv")

df_target = df_enrollment.merge(df_schedule, left_on="SCHEDULE_ID", right_on="ID", how="inner")
df_target.drop(columns=["ID"], inplace=True)

df_target = df_target.merge(df_wos, left_on=["COURSE_DAYS", "SEMESTER"], right_on=["weekday", "semester"], how="inner")
df_target = df_target[["STUDENT_ID", "COURSE_ID", "id"]]
df_target.rename(columns={"STUDENT_ID": "student_id", "COURSE_ID": "course_id", "id": "wos_id"}, inplace=True)
df_target.index.name = "id"

# add value to attendance target to attend the course
df_target["target"] = 1

df_target.to_csv("data staging/target_attendance.csv")