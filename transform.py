import pandas as pd

def flatten_data(data: pd.DataFrame) -> pd.DataFrame:
    """
    Flattens the data so that game genre is separated into different rows.
    """
    data = data.explode("Game_Genres")
    data.reset_index(drop=True)
    return data

def clean_data(data: pd.DataFrame) -> pd.DataFrame:
    """
    Clean the data to remove any weird values.
    """
    data = data.drop(data[data["Game_Genres"] == "\n\nUnder £7\n\n\nUnder £4\n\n"].index)
    data = data.drop(data[data["Game_Genres"] == "NULL"].index)
    data = data.loc[~((data["Playtime_Minutes"] == 0))].reset_index(drop=True)
    return data
