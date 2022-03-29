import pandas as pd

# merge data from target attendance and actual attendance
df_target = pd.read_csv("data staging/target_attendance.csv")
df_target.drop(columns=["id"], inplace=True)

df_actual = pd.read_csv("data staging/actual_attendance.csv")
df_actual.drop(columns=["id"], inplace=True)

df_fact_attendance = df_target.merge(df_actual, on=["student_id", "course_id", "wos_id"], how="left")

# if actual is null, means student did not attend the course, fill it with 0
df_fact_attendance.loc[df_fact_attendance["actual"].isnull(), "actual"] = 0

df_fact_attendance.index.name = "id"
df_fact_attendance.to_csv("data destination/fact_students_attendance.csv")