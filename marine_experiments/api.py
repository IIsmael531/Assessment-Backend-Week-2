"""An API for handling marine experiments."""

from datetime import datetime

from flask import Flask, jsonify, request
from psycopg2 import sql

from database_functions import get_db_connection, get_subject


app = Flask(__name__)

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
    return get_subject()

# Task 1
# A GET request to the / subject end point should return a list of objects(see example below). Each object should have the following information only:

# Subject ID
# Subject Name
# Species Name
# Date of Birth
# Dates should be expressed as strings in the YYYY-MM-DD format.

# Objects should be ordered by date of birth in descending order.


# tables:
# experiment
# psql marine_experiments -c "SELECT * FROM experiment"
# experiment_type
# species
# subject
#


if __name__ == "__main__":
    app.config["DEBUG"] = True
    app.config["TESTING"] = True

    app.run(port=8000, debug=True)

    conn.close()
