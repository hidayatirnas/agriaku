import pandas as pd
from datetime import datetime

# merge all involved data
df_attendance = pd.read_csv("data source/course_attendance.csv")
df_attendance.set_index("ID", inplace=True)
df_attendance["ATTEND_DT"] = df_attendance["ATTEND_DT"].apply(lambda x: datetime.strptime(x, "%d-%b-%y").strftime("%Y-%m-%d"))

df_schedule = pd.read_csv("data staging/schedule.csv")
df_schedule = df_schedule[["ID", "COURSE_ID"]].drop_duplicates()

df_wos = pd.read_csv("data destination/dim_week_of_semester.csv")
df_wos = df_wos[["id", "date"]]

df_actual = df_attendance.merge(df_schedule, left_on="SCHEDULE_ID", right_on="ID", how="inner")
df_actual = df_actual.merge(df_wos, left_on="ATTEND_DT", right_on="date", how="inner")
df_actual = df_actual[["STUDENT_ID", "COURSE_ID", "id"]]
df_actual.rename(columns={"STUDENT_ID": "student_id", "COURSE_ID": "course_id", "id": "wos_id"}, inplace=True)
df_actual.index.name = "id"

# add value to actual attendance
df_actual["actual"] = 1

df_actual.to_csv("data staging/actual_attendance.csv")