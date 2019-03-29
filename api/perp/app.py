import logging

from flask import Flask, jsonify, request

from perp.client import get_mysql_client
from perp.excpetion import PerpException

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)


@app.route("/api/v1/table/<table_name>", methods=["GET"])
def get_all_from_table(table_name):
    client = get_mysql_client()
    try:
        result = client.select_all_from_table(
            table_name,
            request.args.get("order"),
            request.args.get("num_rows"),
            request.args.get("page"),
            request.args.get("page_size")
        )
        return jsonify(result)
    except PerpException as e:
        return error_to_json(e), 400


@app.route("/api/v1/crimes/count", methods=["GET"])
def get_crimes_count():
    client = get_mysql_client()
    try:
        result = client.select_crime_count_by_month(
            request.args.get("month_from"),
            request.args.get("month_to")
        )
        return jsonify(result)
    except PerpException as e:
        return error_to_json(e), 400


@app.route("/api/v1/theft/total_value", methods=["GET"])
def get_total_value_of_thefts():
    client = get_mysql_client()
    try:
        result = client.select_total_value_of_thefts()
        return jsonify(result)
    except PerpException as e:
        return error_to_json(e), 400


@app.route("/api/v1/theft/car/all", methods=["GET"])
def get_neighbourhoods_where_all_car_stolen():
    client = get_mysql_client()
    try:
        result = client.select_neighbourhoods_where_all_car_stolen()
        return jsonify(result)
    except PerpException as e:
        return error_to_json(e), 400


@app.route("/api/v1/criminal/add", methods=["GET"])
def post_criminal():
    client = get_mysql_client()
    try:
        result = client.insert_new_criminal(
            request.args.get("age"),
            request.args.get("height_cm"),
            request.args.get("hair_color"),
            request.args.get("lives_in"),
        )
        return jsonify(result)
    except PerpException as e:
        return error_to_json(e), 400


@app.route("/api/v1/criminal/update/<int:criminal_id>", methods=["GET"])
def patch_criminal(criminal_id):
    client = get_mysql_client()
    try:
        result = client.update_criminal(
            criminal_id,
            request.args.get("age"),
            request.args.get("height_cm"),
            request.args.get("hair_color"),
            request.args.get("lives_in"),
        )
        return jsonify(result)
    except PerpException as e:
        return error_to_json(e), 400


@app.route("/api/v1/criminal/delete/<int:criminal_id>", methods=["GET"])
def delete_criminal(criminal_id):
    client = get_mysql_client()
    try:
        result = client.delete_criminal(criminal_id)
        return jsonify(result)
    except PerpException as e:
        return error_to_json(e), 400


@app.route("/api/v1/criminal/column/<column_name>",  methods=["GET"])
def get_column_from_criminal(column_name):
    client = get_mysql_client()
    try:
        result = client.select_column_from_criminal(
            column_name,
            request.args.get("page"),
            request.args.get("page_size")
        )
        return jsonify(result)
    except PerpException as e:
        return error_to_json(e), 400


@app.route("/api/v1/hello")
def hello_world():
    return jsonify("hello world !")


def error_to_json(error):
    error_dict = {"error": str(error)}
    return jsonify(error_dict)


if __name__ == '__main__':
    app.debug = True
    app.run(port=8000)
