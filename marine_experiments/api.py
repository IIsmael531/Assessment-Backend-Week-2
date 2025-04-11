"""An API for handling marine experiments."""

from datetime import datetime

from flask import Flask, jsonify, request
from psycopg2 import sql

from database_functions import get_db_connection, get_subject, get_experiment


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
    return get_subject(conn)


@app.get("//experiment")
def endpoint_get_experiment():
    """Returns experiment information"""
    return get_experiment(conn)


# A GET request to the / experiment endpoint should return a
# list of objects(see example below). Each object should contain the following information only:

    # experiment_id
    # subject_id
    # Species
    # experiment_date
    # experiment_type_name
    # score

# SELECT experiment_id, subject_id, species_name, TO_CHAR(experiment_date, 'YYYY-MM-DD') AS experiment_date, experiment_type_name,
# ROUND((score::numeric / max_score) * 100, 2)::TEXT || '%' AS score
# FROM experiment
# JOIN subject USING (subject_id)
# JOIN species USING (species_id)
# JOIN experiment_type USING (experiment_type_id)
# ORDER BY experiment_date DESC

    # Score should be expressed as a percentage rounded to 2 d.p.
    # (e.g. "70.34%"). The percentage score should be calculated based on
    # the maximum score for that type of experiment.

    # Dates should be expressed as strings in the YYYY-MM-DD format.

    # Experiments should be sorted in descending order by date.


if __name__ == "__main__":
    app.config["DEBUG"] = True
    app.config["TESTING"] = True

    app.run(port=8000, debug=True)

    conn.close()
