import json
import logging

from flask import Flask

from perp.client import get_mysql_client
from perp.excpetion import PerpException

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)


@app.route("/api/v1/table/<table_name>")
def select_all_from_table(table_name):
    client = get_mysql_client()
    try:
        result = client.select_all_from_table(table_name)
        return json.dumps(result)
    except PerpException as e:
        return str(e), 400


@app.route("/api/v1/hello")
def hello_world():
    return "hello world !"


if __name__ == '__main__':
    app.debug = True
    app.run(port=8000)
