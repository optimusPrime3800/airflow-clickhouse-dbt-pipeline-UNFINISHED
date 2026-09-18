import clickhouse_connect
from pathlib import Path


AIRFLOW_DATA_DIR = Path("/opt/airflow/data")
CLICKHOUSE_DATA_DIR = "/var/lib/clickhouse/user_files"


def get_client():
    return clickhouse_connect.get_client(
        host="clickhouse",
        port=8123,
        username="dbt",
        password="dbt_password",
    )


def load_table(client, file_name, table_name):

    airflow_file = AIRFLOW_DATA_DIR / file_name

    if not airflow_file.exists():
        raise FileNotFoundError(
            f"File not found: {airflow_file}"
        )

    clickhouse_file = (
        f"{CLICKHOUSE_DATA_DIR}/{file_name}"
    )

    print(
        f"\nLoading {file_name} -> raw.{table_name}"
    )

    client.command(
        f"TRUNCATE TABLE raw.{table_name}"
    )

    client.command(
        f"""
        INSERT INTO raw.{table_name}
        SELECT *
        FROM file(
            '{clickhouse_file}',
            Parquet
        )
        """
    )

    result = client.query(
        f"SELECT count() FROM raw.{table_name}"
    )

    count = result.result_rows[0][0]

    print(
        f"raw.{table_name}: {count:,} rows"
    )


def main():

    print("=" * 60)
    print("LOADING PARQUET DATA INTO CLICKHOUSE")
    print("=" * 60)

    client = get_client()

    load_table(
        client,
        "customers.parquet",
        "customers"
    )

    load_table(
        client,
        "products.parquet",
        "products"
    )

    load_table(
        client,
        "orders.parquet",
        "orders"
    )

    load_table(
        client,
        "order_items.parquet",
        "order_items"
    )

    print("\n" + "=" * 60)
    print("CLICKHOUSE LOAD FINISHED")
    print("=" * 60)


if __name__ == "__main__":
    main()