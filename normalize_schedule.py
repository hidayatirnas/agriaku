import pandas as pd

# schedule data needs to be normalized since there are
# multiple data in course_days column

# read file schedule.csv
df_schedule = pd.read_csv("data source/schedule.csv")

# normalize COURSE_DAYS column
df_schedule["COURSE_DAYS"] = df_schedule["COURSE_DAYS"].apply(lambda x: str(x).split(","))
df_schedule = df_schedule.explode("COURSE_DAYS")

# store data to staging folder
df_schedule.to_csv("data staging/schedule.csv", index=None)