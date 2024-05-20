"""Script to extract information from the Steam API and to extract game genres"""
from os import environ
from bs4 import BeautifulSoup

import requests
from requests.exceptions import Timeout, HTTPError

TIMEOUT = 20


def get_owned_games(steam_id: str) -> dict:
    """
    Given a steam id, return a list of the user's owned games.
    """
    url = f"https://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={environ['STEAM_API_KEY']}&steamid={steam_id}&format=json&include_appinfo=true"
    try:
        response = requests.get(url, timeout=TIMEOUT)
    except ConnectionError as exc:
        raise ConnectionError("Connection failed") from exc
    except Timeout as exc:
        raise Timeout("The request timed out.") from exc
    except HTTPError as exc:
        raise HTTPError("url is invalid.") from exc

    return response.json()


def get_games_info(data: dict) -> list:
    """
    Given JSON data from calling the Steam API, return the names and ids of the games.
    """
    result = []
    for game in data["response"]["games"]:
        result.append({"id": game["appid"],
                       "name": game["name"],
                       "playtime": game["playtime_forever"]})
    return result


def get_html(game_id: str) -> str:
    """
    Given a Steam game id, return the HTML for the game's webpage.
    """
    url = f"https://store.steampowered.com/app/{game_id}/"
    try:
        response = requests.get(url, timeout=TIMEOUT)
    except ConnectionError as exc:
        raise ConnectionError("Connection failed") from exc
    except Timeout as exc:
        raise Timeout("The request timed out.") from exc
    except HTTPError as exc:
        raise HTTPError("url is invalid.") from exc

    return response.text


def extract_genre(html: str) -> str:
    """
    Given HTML of a game's Steam webpage, return the genres associated with it.
    """
    soup = BeautifulSoup(html, "lxml")
    genres = soup.find(
        "span", {"data-panel": '{"flow-children":"row"}'})
    # If there are no genres associated with the game
    if not genres:
        return "NULL"
    return genres.text.split(", ")
