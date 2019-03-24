import logging

from flask import Flask, jsonify, request

from perp.client import get_mysql_client
from perp.excpetion import PerpException

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)


@app.route("/api/v1/table/<table_name>", methods=["GET"])
def select_all_from_table(table_name):
    client = get_mysql_client()
    try:
        result = client.select_all_from_table(
            table_name,
            request.args.get("order"),
            request.args.get("num_rows")
        )
        return jsonify(result)
    except PerpException as e:
        return jsonify(str(e)), 400


@app.route("/api/v1/hello")
def hello_world():
    return jsonify("hello world !")


if __name__ == '__main__':
    app.debug = True
    app.run(port=8000)
