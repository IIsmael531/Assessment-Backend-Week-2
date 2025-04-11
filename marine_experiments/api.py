"""An API for handling marine experiments."""

from datetime import datetime

from flask import Flask, jsonify, request
from psycopg2 import sql

from database_functions import get_db_connection, get_subject, get_experiment


app = Flask(__name__)


def validate_type(type):
    """Return if type query is valid"""
    return type.lower() in {"intelligence", "obedience", "aggression"}


def validate_score_over(score_over):
    """Return if score query is valid"""
    try:
        score = int(score_over)
        return 0 <= score <= 100
    except ValueError:
        return False


"""
For testing reasons; please ALWAYS use this connection. 
- Do not make another connection in your code
- Do not close this connection
"""
conn = get_db_connection("marine_experiments")


@app.get("/")
def home():
    """Returns an informational message."""
    return jsonify({
        "designation": "Project Armada",
        "resource": "JSON-based API",
        "status": "Classified"
    })


@app.get("/subject")
def endpoint_get_subject():
    """Returns subject information"""
    return get_subject(conn)


@app.get("/experiment")
def endpoint_get_experiment():
    """Returns experiment information"""
    type = request.args.get("type", None)
    score_over = request.args.get("score_over", None)

    # checking for errors
    if type and not validate_type(type):
        return {'error': "Invalid value for 'type' parameter"}, 400

    if score_over and not validate_score_over(score_over):
        return {'error': "Invalid value for 'score_over' parameter"}, 400

    return get_experiment(conn, type, score_over)


# Task 3
# A GET request to the / experiment endpoint should accept
# two optional query parameters.

# Both parameters accept only specific values
# invalid values should result in a 400 response with a JSON response object of the format {"error": "Invalid value for 'x' parameter"}.
# If both parameters are passed at once, their effects should combine.
# By default, without the arguments, the endpoint should return a full list of experiments.


# type
# This parameter should accept only "intelligence", "obedience" or "aggression"
# as values(not case-sensitive). When a valid value is passed to the type parameter,
# only experiments of that type should be returned.

# score_over
# This parameter should accept only integer values in the range 0-100.
# When a valid value is passed to the score_over parameter, only experiments
# where the percentage score was greater than the value should be returned.


if __name__ == "__main__":
    app.config["DEBUG"] = True
    app.config["TESTING"] = True

    app.run(port=8000, debug=True)

    conn.close()
