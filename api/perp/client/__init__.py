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

    def _insert(self, insert_query_string):
        """
        Execute the query string
        :param insert_query_string: The insert query to execute
        :raises PerpException on any DatabaseError
        """
        if not self._connect():
            raise PerpException("Unable to connect to database")

        logging.debug(f"Querying database with query: {insert_query_string}")

        try:
            with self.connection.cursor() as cursor:
                cursor.execute(insert_query_string)
            self.connection.commit()
        except pymysql.err.DatabaseError as e:
            logging.error(e)
            raise PerpException("Error occurred while executing query")

    def _select_count_from_table(self, table_name):
        """
        Return the number of entries in the given table
        :param table_name: The table of the table to count
        :return: The number of entries
        """
        query_string = f"SELECT count(*) AS num_rows FROM {table_name}"
        result = self._select(query_string)[0]["num_rows"]
        return result

    def select_all_from_table(
        self,
        table_name,
        order_by=None,
        num_rows=None,
        page=None,
        page_size=None
    ):
        """
        Select all rows from a given table
        :param table_name: The name of the table
        :param order_by: The name of the column to sort by
        :param num_rows: The number of rows to select
        :param page: The number of the page to select.
        :param page_size: The number of results per page
        :return: A list of dicts representing the rows of the result
        """
        if page and num_rows:
            raise PerpException(
                "Both page and num_rows cannot be specified"
            )

        query_string = f"SELECT * FROM {table_name}"
        query_string += f" ORDER BY {order_by}" if order_by else ""
        query_string += f" LIMIT {num_rows}" if num_rows else ""

        if page is not None:
            page = MysqlClient._to_int(page=page)
            page_size = MysqlClient._to_int(page_size=page_size or 10)
            page_offset = page_size * page

            total_size = self._select_count_from_table(table_name)

            if (page_offset < 0) or (page_offset >= total_size):
                raise PerpException(f"Page index {page} out of range")

            query_string += f" LIMIT {page_offset}, {page_size}"

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

    def select_total_value_of_thefts(self):
        """
        Aggregate the total value of items stolen across all thefts.
        :return: The total value of items stolen.
        """
        query_string = """
        SELECT sum(i_value) total_value
        FROM StolenItem s JOIN Item i ON s.i_name = i.i_name
        """
        return self._select(query_string)[0]

    def insert_new_criminal(self, age, height_cm, hair_color, lives_in):
        """
        Insert a new criminal into the Criminal table
        :param age: The criminal's height
        :param height_cm: The criminal's age
        :param hair_color: The criminal's hair color
        :param lives_in: The ID of the neighbourhood the criminal lives in
        :return: The record that has been added
        """
        if None in (age, height_cm, hair_color, lives_in):
            raise PerpException(
                "All of age, height_cm, hair_color, lives_in must be specified"
            )

        max_id_query_string = "SELECT max(Criminal_ID) max_id from Criminal"
        max_id = self._select(max_id_query_string)[0]["max_id"]
        new_id = max_id + 1

        query_string = "INSERT INTO Criminal VALUES ({}, {}, {}, '{}', {})"
        self._insert(query_string.format(
            new_id, age, height_cm, hair_color, lives_in
        ))

        select_string = f"SELECT * FROM Criminal WHERE Criminal_ID = {new_id}"
        return self._select(select_string)[0]

    def update_criminal(
            self,
            criminal_id,
            age=None,
            height_cm=None,
            hair_color=None,
            lives_in=None
    ):
        """
        Update the criminal that has criminal_id
        :param criminal_id: The id of the criminal to update
        :param age: The age to update to
        :param height_cm: The height to update to
        :param hair_color: The hair color to update to
        :param lives_in: The Neighbourhood ID to update to
        :return: A dict of the updated tuple
        """
        query_string = "UPDATE Criminal SET {} WHERE Criminal_ID = {}"
        updates = f"age = {age}, " if age else ""
        updates += f"height_cm = {height_cm}, " if height_cm else ""
        updates += f"hair_color = '{hair_color}', " if hair_color else ""
        updates += f"lives_in = {lives_in}" if lives_in else ""
        updates = updates.strip(", ")

        if not updates:
            raise PerpException(
                "One of age, height_cm, hair_color, lives_in must be specified"
            )

        self._insert(query_string.format(updates, criminal_id))

        select_string = f"""
        SELECT * FROM Criminal WHERE Criminal_ID = {criminal_id}
        """
        updated_res = self._select(select_string)
        if len(updated_res) == 0:
            raise PerpException(
                f"No Criminal exists with ID = {criminal_id}"
            )
        return updated_res[0]

    def delete_criminal(self, criminal_id):
        """
        Delete the criminal with criminal_id.
        :param criminal_id: The ID to delete
        :return: A dict of the ID that was deleted.
        Will not check that something is actually deleted.
        """
        query_string = f"DELETE FROM Criminal WHERE Criminal_ID = {criminal_id}"
        self._insert(query_string)
        return {"criminal_deleted": criminal_id}

    @staticmethod
    def _to_int(**kwargs):
        key, value = next(iter(kwargs.items()))
        try:
            res = int(value)
        except (ValueError, TypeError):
            raise PerpException(f"Parameter {key} must be an integer")
        return res
