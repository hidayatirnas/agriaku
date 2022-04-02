import pandas as pd

# load all fact and dimension tables
df_fact_students_attendance = pd.read_csv("data destination/fact_students_attendance.csv")
df_dim_wos = pd.read_csv("data destination/dim_week_of_semester.csv")
df_dim_course = pd.read_csv("data source/course.csv")

# merge all tables
df_final = df_fact_students_attendance.merge(df_dim_wos, left_on="wos_id", right_on="id", how="inner")
df_final = df_final.merge(df_dim_course, left_on="course_id", right_on="ID", how="inner")

# do transformations
df_final = df_final[["student_id", "week", "semester", "NAME", "target", "actual"]]
df_final.rename(columns={"semester": "SEMESTER_ID", "week": "WEEK_ID", "NAME": "COURSE_NAME"}, inplace=True)

# prepare the summary
df_summary = df_final.groupby(by=["SEMESTER_ID", "COURSE_NAME", "WEEK_ID"])[["target", "actual"]].sum()
df_summary["ATTENDANCE_PCT"] = df_summary["actual"] / df_summary["target"] * 100
df_summary.drop(columns=["target", "actual"], inplace=True)

df_summary.to_csv("summary.csv", index=True)