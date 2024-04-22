"""Script to generate a list of valid Steam Ids."""
from os import environ
import random
from time import perf_counter

import requests
from requests.exceptions import Timeout, HTTPError

TIMEOUT = 20
START_RANGE = 76561197000000000

def get_valid_random_ids(steam_ids: str) -> list:
    """
    From the randomly generated steam ids, check to see which ones are actually valid.
    """
    url = f"http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={environ['STEAM_API_KEY']}&steamids={steam_ids}"
    try:
        response = requests.get(url, timeout=TIMEOUT)
    except ConnectionError as exc:
        raise ConnectionError("Connection failed") from exc
    except Timeout as exc:
        raise Timeout("The request timed out.") from exc
    except HTTPError as exc:
        raise HTTPError("url is invalid.") from exc
    
    info = response.json()

    if not info["response"]["players"]:
        return None
    
    result = []
    for player in info["response"]["players"]:
        result.append(player["steamid"])
    return result


def valid_steam_id(current_steam_id_list: list, steam_id: str) -> bool:
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
    
    if steam_id in current_steam_id_list:
        return False

    return True


def generate_random_ids() -> list:
    """
    Generates 100 random potential Steam ID.
    """
    return [str(random.randint(START_RANGE, 76561199999999999)) for _ in range(100)]


def convert_list_to_string(steam_ids: list) -> str:
    """
    Converts the list of random steam ids into a comma separated string.
    """
    string = steam_ids[0]
    for id in steam_ids[1:]:
        string = string + "," + id
    return string


def get_steam_ids() -> list:
    """
    Returns all the current steam ids that we have collected so far.
    """
    with open("steam_ids.txt", "r") as file:
        content = file.read().splitlines()
    return content


def generate_valid_steam_ids(number_to_generate: int) -> None:
    """
    Create a list of 1000 valid steam ids then export it to a text file.
    """
    all_steam_ids = get_steam_ids()
    start = perf_counter()
    counter = 0
    steam_ids = []
    while counter != number_to_generate:
        random_ids = generate_random_ids()
        try:
            valid_ids = get_valid_random_ids(random_ids)
            while not valid_ids:
                valid_ids = get_valid_random_ids(random_ids)

            for id in valid_ids:
                if valid_steam_id(all_steam_ids, id):
                    steam_ids.append(str(id))
                    counter += 1
                    print(f"ID: {id} is valid. {counter}/{number_to_generate} found...")
                    if counter == number_to_generate:
                        break
        except Exception as err:
            print(f"Error occured: {err}")

    file = open("steam_ids.txt", "a")
    for id in steam_ids:
        file.write(id + "\n")
    file.close()
    print("Id generation done! Time Elapsed: ", perf_counter() - start)

