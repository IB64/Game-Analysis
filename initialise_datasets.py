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
            bigquery.SchemaField("id", "INT64", mode="REQUIRED"),
            bigquery.SchemaField("user_id", "INT64", mode="REQUIRED"),
            bigquery.SchemaField("game_id", "INT64", mode="REQUIRED"),
            bigquery.SchemaField("playtime", "INT64", mode="REQUIRED")
        ]

        schema_2 = [
            bigquery.SchemaField("id", "INT64", mode="REQUIRED"),
            bigquery.SchemaField("app_id", "INT64", mode="REQUIRED"),
            bigquery.SchemaField("name", "STRING", mode="REQUIRED")
        ]

        schema_3 = [
            bigquery.SchemaField("id", "INT64", mode="REQUIRED"),
            bigquery.SchemaField("game_id", "INT64", mode="REQUIRED"),
            bigquery.SchemaField("genre_id", "INT64", mode="REQUIRED")
        ]

        schema_4 = [
            bigquery.SchemaField("id", "INT64", mode="REQUIRED"),
            bigquery.SchemaField("name", "INT64", mode="REQUIRED")
        ]

        table_ref_1 = client.dataset(dataset_id).table(table_id_1)
        table_ref_2 = client.dataset(dataset_id).table(table_id_2)
        table_ref_3 = client.dataset(dataset_id).table(table_id_3)
        table_ref_4 = client.dataset(dataset_id).table(table_id_4)

        table_1 = bigquery.Table(table_ref_1, schema=schema_1)
        table_2 = bigquery.Table(table_ref_2, schema=schema_2)
        table_3 = bigquery.Table(table_ref_3, schema=schema_3)
        table_4 = bigquery.Table(table_ref_4, schema=schema_4)
        
        try:
            client.create_table(table_1, exists_ok=True)
            print(f"Table {table_id_1} created successfully in dataset {dataset_id}.")
            client.create_table(table_2, exists_ok=True)
            print(f"Table {table_id_2} created successfully in dataset {dataset_id}.")
            client.create_table(table_3, exists_ok=True)
            print(f"Table {table_id_3} created successfully in dataset {dataset_id}.")
            client.create_table(table_4, exists_ok=True)
            print(f"Table {table_id_4} created successfully in dataset {dataset_id}.")
        except Exception as e:
            print(f"Error creating table: {e}")


if __name__ == "__main__":
    load_dotenv()
    create_dataset()
    create_tables()