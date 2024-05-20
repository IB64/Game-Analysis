import json
from time import perf_counter

from dotenv import load_dotenv
import pandas as pd

import generate_ids as ge
import extract as ex
import transform as tr

GENRE_FILE_PATH = "../data/genres.json"


def extract(amount_to_extract: int) -> list:
    """
    Extracts data from a list of steam ids.
    """
    number_skipped = 0
    if amount_to_extract > 0:
        steam_ids = ge.get_steam_ids()[-amount_to_extract:]
    else:
        steam_ids = ge.get_ultimate_steam_ids()
    number_of_ids = len(steam_ids)
    print(f"Starting Extraction... Extracting from {number_of_ids} ids...")
    games_data = []
    # load genre data
    with open(GENRE_FILE_PATH, "r") as file:
        genres = json.load(file)

    for index, person in enumerate(steam_ids):
        try:
            owned_games = ex.get_owned_games(person)
            games = ex.get_games_info(owned_games)

            for game in games:
                try:
                    game_genres = genres[str(game["id"])]
                except:
                    web_page = ex.get_html(game["id"])
                    game_genres = ex.extract_genre(web_page)
                    genres[game["id"]] = game_genres

                games_data.append({
                    'User_Id': person,
                    'Game_Id': game['id'],
                    'Game_Name': game['name'],
                    'Game_Genres': game_genres,
                    'Playtime_Minutes': game['playtime']
                })

            print(f"Person {index+1}/{number_of_ids} done...")
        except Exception as err:
            print(f"Error occured: {err}. Person {index+1} Skipped...")
            number_skipped += 1
    print("Extraction Finished!")
    print(f"Number of people skipped: {number_skipped}")

    # Export genres to local machine as a json file
    with open(GENRE_FILE_PATH, "w") as file:
        json.dump(genres, file, indent=4)
    print(f"Genres exported successfully to: {GENRE_FILE_PATH}")

    return games_data


def transform(data: list) -> pd.DataFrame:
    """
    Converts the data from extraction into a data frame and cleans it.
    """
    print("Starting Transformation...")
    data_df = pd.DataFrame(data)
    data_df = tr.flatten_data(data_df)
    print("Data flattened...")
    data_df = tr.clean_data(data_df)
    print("Data cleaned...")
    print("Transformation finished!")
    return data_df


if __name__ == "__main__":
    load_dotenv()
    answer = input(
        "Do you want to generate new steam ids? Please type 'yes' or 'no': ").lower()

    if answer == "yes":
        number_to_generate = int(input(
            "Please type how many new ids you would like to generate: "))
        ge.generate_valid_steam_ids(number_to_generate)
    else:
        number_to_generate = 0
    start = perf_counter()

    data = extract(number_to_generate)
    clean_data = transform(data)
    if number_to_generate == 0:
        clean_data.to_csv("clean_game_data.csv", encoding='utf-8', index=False)
    else:
        clean_data.to_csv("clean_game_data.csv", mode="a", encoding='utf-8', index=False, header=False)
    print(f"Done! Time Elapsed: {perf_counter() - start} seconds.")
