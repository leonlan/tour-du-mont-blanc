from datetime import datetime, timedelta
import json

import requests

from .constants import API_URL


def get_availability(date: str, id: int | str) -> dict[datetime, int]:
    """
    Gets the availability of a given date and a given id.

    Parameters
    ----------
    date: str
        The date in the format YYYY-MM-DD.
    id: int | str
        The id of the refuge.

    Returns
    -------
    dict[datetime, int]
        A dictionary with the bed availability for each day starting from
        ``date`` until 30 days after.
    """
    # The API returns availability for 15 days starting from ``date`` - 15 days.
    # We need to add 15 days to the date to get the correct availability.
    start_date = datetime.strptime(date, "%Y-%m-%d")
    reference_date = (start_date + timedelta(days=15)).strftime("%Y-%m-%d")

    url = API_URL.format(date=reference_date, id=id)
    response = requests.get(url)

    # Removing outer braces make the response a valid json
    text = response.text.lstrip("(").rstrip(")")
    data = json.loads(text)[0]

    return {
        start_date + timedelta(days=idx): int(avail["s"])
        for idx, avail in enumerate(data["planning"])
    }
