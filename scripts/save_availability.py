from collections import defaultdict
from datetime import datetime
from pathlib import Path

import pandas as pd

import tmb

data_loc = Path("data/huts.csv")
refuges_df = pd.read_csv(data_loc)
refuges_df = refuges_df[refuges_df["id"].notnull()]

dates = ["2024-06-01", "2024-07-01", "2024-07-31"]
availability = defaultdict(dict)

for date in dates:
    for idx, data in refuges_df.iterrows():
        part = tmb.get_availability(date, int(data["id"]))
        availability[data["mon_name"]].update(part)


df = pd.DataFrame(availability).T
df.columns = df.columns.date

today = datetime.now().strftime("%Y%m%d")
df.to_csv("calendar/availability.csv")
