

from faker import Faker

import logging

from airflow.operators import PythonOperator
from aiflow.providers.clickhouse.hook.clickhouse import ClickHouseHook


# faker = Faker()





def create_table():

    hook = ClickHouseHook(clickhouse_id="default")

    create_db = "CREATE DATABASE IF NOT EXISTS analytics"

    create_table = """ 
        CREATE TABLE analytics.orders
    (
        order_id UUID,
        user_id UUID,
        product_id UUID,
        category String,
        price Float64,
        status String,
        region String,
        order_date DateTime
    )
    ENGINE = MergeTree()
    PARTITION BY toYYYYMM(order_date)
    ORDER BY(order_date, region)
    """
    hook.run(create_db)
    hook.run(create_table)


   


def create_fake_data():

