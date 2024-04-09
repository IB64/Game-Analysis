"""Script to generate a list of valid Steam Ids."""
from os import environ
import random
from time import perf_counter

import requests
from requests.exceptions import Timeout, HTTPError

TIMEOUT = 20
START_RANGE = 76561197000000000


def valid_steam_id(steam_id: str) -> bool:
    """
    Given a string for steam id, check if it's valid. Return True if it is, otherwise false.
    """
    url = f"http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={environ['STEAM_API_KEY']}&steamid={steam_id}&format=json"
    try:
        response = requests.get(url, timeout=TIMEOUT)
    except ConnectionError as exc:
        raise ConnectionError("Connection failed") from exc
    except Timeout as exc:
        raise Timeout("The request timed out.") from exc
    except HTTPError as exc:
        raise HTTPError("url is invalid.") from exc

    # Invalid steam id returns code 400 and 404
    if response.status_code in (400, 404):
        return False

    info = response.json()
    if not info["response"]:
        return False

    # Steam id with 0 games
    if info["response"]["game_count"] == 0:
        return False

    return True


def generate_random_id() -> str:
    """
    Generates a potential Steam ID.
    """
    return random.randint(START_RANGE, 76561199999999999)


def generate_valid_steam_ids(number_to_generate: int) -> None:
    """
    Create a list of 1000 valid steam ids then export it to a text file.
    """
    start = perf_counter()
    counter = 0
    steam_ids = []
    while counter != number_to_generate:
        random_id = generate_random_id()
        if valid_steam_id(random_id):
            steam_ids.append(str(random_id))
            counter += 1
            print(f"Valid Id number: {counter} found...")

    file = open("steam_ids.txt", "w")
    for id in steam_ids:
        file.write(id + "\n")
    file.close()
    print("Id generation done! Time Elapsed: ", perf_counter() - start)
