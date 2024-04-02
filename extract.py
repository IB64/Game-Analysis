"""Script to extract information from the Steam API and to extract game genres"""
import pandas as pd
from os import environ
from bs4 import BeautifulSoup
from dotenv import load_dotenv
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


def get_games_info(data: dict) -> dict:
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
    return genres.text

def get_steam_ids() -> list:
    with open("steam_ids.txt", "r") as file:
        content = file.read().splitlines()
    return content


if __name__ == "__main__":
    load_dotenv()

    # gets list of all games
    steam_ids = get_steam_ids()
    games_data = [] #empty list
    for person in steam_ids:
        owned_games = get_owned_games(person)
        games = get_games_info(owned_games)
    
        for game in games:
            web_page = get_html(game["id"])
            game_genres = extract_genre(web_page)
            games_data.append({
                'GameId': game['id'],
                'Game_Name': game['name'],
                'Game_Genres': game_genres,
                'Playtime_Minutes': game['playtime']
                })
            
    df = pd.DataFrame(games_data)
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)

    df.to_csv('game_data.csv', index=False)

    print(df)        
            #print(game["name"])
            #print(game["id"])
            #print(game["playtime"])
            #print(f"{game_genres}")