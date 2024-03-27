from bs4 import BeautifulSoup

import requests
from requests.exceptions import Timeout, HTTPError

TIMEOUT = 20


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


if __name__ == "__main__":
    # Dragon's Dogma 2
    web_page = get_html("2054970")
    genres = extract_genre(web_page)
    print(genres)
