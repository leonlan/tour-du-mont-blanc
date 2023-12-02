import datetime

import requests

from .constants import API_URL


def get_availability(date: str, id: int) -> dict[str, str]:
    """
    Gets the availability of a given date and a given id
    """
    url = API_URL.format(date=date, id=id)
    response = requests.get(url)

    breakpoint()

    # 32405
    # 2023-12-03
    # object 15 is the first available date of miniapp of the website
