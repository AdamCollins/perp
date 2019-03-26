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

    def _select(self, query_string):
        """
        Query the database are return all results
        :param query_string: The query to execute
        :return: All results
        """
        if not self._connect():
            raise PerpException("Unable to connect to database")

        logging.debug(f"Querying database with query: {query_string}")

        try:
            with self.connection.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute(query_string)
                result = cursor.fetchall()
        except pymysql.err.DatabaseError as e:
            logging.error(e)
            raise PerpException("Error occurred while executing query")
        return result

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
        query_string = f"SELECT * FROM {table_name}"
        query_string += f" ORDER BY {order_by}" if order_by else ""
        query_string += f" LIMIT {num_rows}" if num_rows else ""

        return self._select(query_string)

    def select_crime_count_by_year(self, year_from=None, year_to=None):
        """
        Count the number of crimes per year grouped by crime type
        :param year_from: The start of the range of years
        :param year_to: The end of the range of years
        :return: A list of dict results
        """
        query_string = """
        SELECT allyears.c_year,
            COALESCE(num_collision, 0) AS num_collision,
            COALESCE(num_theft, 0) AS num_theft,
            COALESCE(num_other, 0) AS num_other
        FROM (
            SELECT DISTINCT YEAR(c_datetime) AS c_year FROM Crime {}
        ) allyears LEFT JOIN (
            SELECT YEAR(c.c_datetime) AS c_year, count(*) AS num_collision
            FROM Crime c JOIN VehicleCollision vc ON c.Crime_ID = vc.Crime_ID
            GROUP BY c_year
        ) collisions ON allyears.c_year = collisions.c_year LEFT JOIN (
            SELECT YEAR(c.c_datetime) AS c_year, count(*) AS num_theft
            FROM Crime c JOIN Theft t ON c.Crime_ID = t.Crime_ID
            GROUP BY c_year
        ) thefts ON allyears.c_year = thefts.c_year LEFT JOIN (
            SELECT YEAR(c.c_datetime) AS c_year, count(*) AS num_other
            FROM Crime c
            WHERE c.Crime_ID NOT IN (
                SELECT Crime_ID FROM VehicleCollision
                UNION
                SELECT Crime_ID FROM Theft
            ) GROUP BY c_year
        ) other ON allyears.c_year = other.c_year
        ORDER BY allyears.c_year
        """
        if year_from:
            having = f"HAVING c_year >= {year_from}"
            having += f" AND c_year <= {year_to}" if year_to else ""
        elif year_to:
            having = f"HAVING c_year <= {year_to}"
        else:
            having = ""

        return self._select(query_string.format(having))
