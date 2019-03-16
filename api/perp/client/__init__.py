from functools import lru_cache
import logging

import pymysql

from perp.config import Config
from perp.excpetion import PerpException


@lru_cache(maxsize=1)
def get_mysql_client():
    config = Config()
    return MysqlClient(
        host=config.get_config_option("database", "host"),
        user=config.get_config_option("database", "user"),
        password=config.get_config_option("database", "password"),
        db=config.get_config_option("database", "name")
    )


class MysqlClient:

    def __init__(self, host, user, password, db):
        self.connection = pymysql.connect(
            host=host,
            user=user,
            password=password,
            db=db
        )

    def select_all_from_table(
            self,
            table_name,
            order_by=None,
            num_rows=None
    ):
        """
        Select all rows from a given table
        :param table_name: The name of the table
        :param order_by: The name of the column to sort by
        :param num_rows: The number of rows to select
        :return: A list of dicts representing the rows of the result
        """

        self.connection.ping(reconnect=True)

        query_string = f"SELECT * FROM {table_name}"
        query_string += f" ORDER BY {order_by}" if order_by else ""
        query_string += f" LIMIT {num_rows}" if num_rows else ""

        try:
            with self.connection.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute(query_string)
                result = cursor.fetchall()
        except pymysql.err.DatabaseError as e:
            logging.error(e)
            raise PerpException
        return result
