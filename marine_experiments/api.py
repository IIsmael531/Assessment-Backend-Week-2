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


if __name__ == "__main__":
    app.config["DEBUG"] = True
    app.config["TESTING"] = True

    app.run(port=8000, debug=True)

    conn.close()
