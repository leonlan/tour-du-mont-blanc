import os
import re

directory = "."  # replace with your directory

for filename in os.listdir(directory):
    if re.match(r"\d{8}_availability", filename):
        date = re.findall(r"\d{8}", filename)[0]
        formatted_date = "{}-{}-{}".format(date[:4], date[4:6], date[6:8])
        new_name = filename.replace(date, formatted_date).replace("_availability", "")
        os.rename(os.path.join(directory, filename), os.path.join(directory, new_name))
