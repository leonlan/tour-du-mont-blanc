# Tour du Mont Blanc
`tmb` is a Python application to help you plan your Tour du Mont Blanc (TMB) hike.

I built this tool because I wanted to check the availability of refuges on a specific route starting on a specific date (say 1 July 2023).
Most refuges on the TMB list their availability on https://www.montourdumontblanc.com, but the website is a hard to navigate.
You would have to find each refuge, click the calendar up to some date and then figure out if everything is aligned.
Instead, this application will help you to make an availability calendar for each of the requested refuges, showing in one glance if the planned itinerary is possible or not.

## Example usage
Make sure you have all dependencies installed (setup using `poetry install` or install dependencies manually).

Run the following script to get the availability of all huts from 1 July 2024 till 30 August 2024.

``` python
from collections import defaultdict
from datetime import datetime
from pathlib import Path

import pandas as pd

import tmb

data_loc = Path("data/refuges.csv")
refuges_df = pd.read_csv(data_loc)

dates = ["2024-07-01", "2024-07-31"]
availability = defaultdict(dict)

for date in dates:
    for idx, data in refuges_df.iterrows():
        part = tmb.get_availability(date, data["id"])
        availability[data["name"]].update(part)

df = pd.DataFrame(availability).T
df.columns = df.columns.date

df.to_csv(f"availability.csv")
tmb.plot(df, save_loc=f"availability.pdf")
```

This will save a CSV file with the number of beds per refuge for each requested day, and it will produce a plot of the availability as a calendar like this:

![example_plot](./example_plot.png)
    
## Notes
- Not all refuges on the TMB have their availability listed on https://www.montourdumontblanc.com.
- If you follow the standard TMB stages, most of the popular refuges are already fully booked by November. You will need to plan an itinerary that doesn't follow the classic TMB stages. (See https://tourdumontblanchike.com/tour-du-mont-blanc-etapes-stages/ about the stages).
