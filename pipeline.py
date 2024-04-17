from time import perf_counter

from dotenv import load_dotenv
import pandas as pd

import generate_ids as ge
import extract as ex
import transform as tr


def extract() -> list:
    """
    Extracts data from a list of steam ids.
    """
    steam_ids = ge.get_steam_ids()
    number_of_ids = len(steam_ids)
    print(f"Starting Extraction... Extracting from {number_of_ids} ids...")
    games_data = []
    genres = {}
    for index, person in enumerate(steam_ids):
        owned_games = ex.get_owned_games(person)
        games = ex.get_games_info(owned_games)

        for game in games:
            try:
                game_genres = genres[game["id"]]
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
    print("Extraction Finished!")
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
    start = perf_counter()

    data = extract()
    clean_data = transform(data)
    clean_data.to_csv("clean_game_data.csv", encoding='utf-8', index=False)
    print(f"Done! Time Elapsed: {perf_counter() - start} seconds.")
