import json

from flask import Flask

from ecs_test_app.client import get_mysql_client
from ecs_test_app.excpetion import PerpException

app = Flask(__name__)


@app.route("/api/v1/table/<table_name>")
def select_all_from_table(table_name):
    select_string = f"SELECT * FROM {table_name}"
    client = get_mysql_client()
    try:
        result = client.select(select_string)
        return json.dumps(result)
    except PerpException:
        return f'Table with name "{table_name}" does not exist', 400


@app.route("/api/v1/hello")
def hello_world():
    return "hello world !"


if __name__ == '__main__':
    app.debug = True
    app.run(port=8000)
