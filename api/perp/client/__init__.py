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
        logging.info(
            f"Connecting to database {db} at {host} as {user}"
        )
        self.host = host
        self.user = user
        self.password = password
        self.db = db
        self._connect()

    def _connect(self):

        try:
            if hasattr(self, "connection") and self.connection is not None:
                self.connection.ping(reconnect=True)
            else:
                    self.connection = pymysql.connect(
                        host=self.host,
                        user=self.user,
                        password=self.password,
                        db=self.db
                    )
                    if self.connection.open:
                        logging.info(f"Connection to database successful")
        except pymysql.err.OperationalError as e:
            self.connection = None
            logging.error(e)
            logging.error(f"Unable to connect to database")
            return False
        return True

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

        if not self._connect():
            raise PerpException("Unable to connect to database")

        query_string = f"SELECT * FROM {table_name}"
        query_string += f" ORDER BY {order_by}" if order_by else ""
        query_string += f" LIMIT {num_rows}" if num_rows else ""

        logging.info(f"Querying database with query: {query_string}")

        try:
            with self.connection.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute(query_string)
                result = cursor.fetchall()
        except pymysql.err.DatabaseError as e:
            logging.error(e)
            raise PerpException("Error occurred while executing query")
        return result
