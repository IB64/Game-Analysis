"Script to generate the tables you need within a GCP dataset."
from os import environ

from dotenv import load_dotenv
from google.cloud import bigquery


def create_dataset() -> None:
    """
    Create the dataset to store the tables for the project.
    """

    with bigquery.Client() as client:
        dataset_id = environ["DATA_SET_ID"]
        project_id = environ["PROJECT_ID"]

        dataset = bigquery.Dataset(f"{project_id}.{dataset_id}")

        dataset.location = "europe-west2"

        client.create_dataset(dataset, exists_ok=True)


def create_tables() -> None:
    """
    Create the tables needed for the project based on the schema.
    """
    table_id_1 = "record"
    table_id_2 = "game"
    table_id_3 = "game_genre"
    table_id_4 = "genre"

    with bigquery.Client() as client:
        dataset_id = environ["DATA_SET_ID"]

        schema_1 = [
            bigquery.SchemaField("id", "NUMERIC"),
            bigquery.SchemaField("user_id", "BIGNUMERIC"),
            bigquery.SchemaField("game_id", "NUMERIC"),
            bigquery.SchemaField("playtime", "NUMERIC"),
        ]

        table_ref = client.dataset(dataset_id).table(table_id_1)

        table = bigquery.Table(table_ref, schema=schema_1)
        
        try:
            client.create_table(table)
            print(f"Table {table_id_1} created successfully in dataset {dataset_id}.")
        except Exception as e:
            print(f"Error creating table: {e}")


if __name__ == "__main__":
    load_dotenv()
    create_dataset()
    create_tables()