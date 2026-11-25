# Owner: Jackson / Jaymin
# PyMySQL connection, sets time_zone to UTC

import pymysql
from backend.config import (
    DB_HOST,
    DB_PORT,
    DB_USER,
    DB_PASSWORD,
    DB_NAME
)


def get_db_connection():
    connection = pymysql.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        cursorclass=pymysql.cursors.DictCursor
    )

    with connection.cursor() as cursor:
        cursor.execute("SET time_zone = '+00:00'")

    return connection