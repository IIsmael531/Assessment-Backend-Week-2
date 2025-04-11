"""Functions that interact with the database."""

from psycopg2 import connect
from psycopg2.extras import RealDictCursor
from psycopg2.extensions import connection, cursor


def get_db_connection(dbname,
                      password="postgres") -> connection:
    """Returns a DB connection."""
    return connect(dbname=dbname,
                   host="localhost",
                   port=5432,
                   password=password,
                   cursor_factory=RealDictCursor)


def get_cursor(conn: connection) -> cursor:
    """Returns a cursor object using the provided database connection."""
    return conn.cursor()


def get_subject(conn) -> list[dict]:
    """Returns all subject details"""
    cursor = get_cursor(conn)

    query = """
    SELECT subject_id, subject_name, species_name, TO_CHAR(date_of_birth, 'YYYY-MM-DD') AS date_of_birth
    FROM subject 
    JOIN species USING(species_id)
    ORDER BY date_of_birth DESC"""

    cursor.execute(query,)
    rows = cursor.fetchall()
    cursor.close()

    return [r for r in rows]


def get_experiment(conn):
    """Returns all experiment details"""
    cursor = get_cursor(conn)

    query = """    
    SELECT experiment_id, subject_id, species_name AS species, TO_CHAR(experiment_date, 'YYYY-MM-DD') AS experiment_date, type_name AS experiment_type, ROUND((score::numeric / max_score) * 100, 2)::TEXT || '%' AS score
    FROM experiment
    JOIN subject USING (subject_id)
    JOIN species USING (species_id)
    JOIN experiment_type USING (experiment_type_id)
    ORDER BY experiment_date DESC"""

    cursor.execute(query,)
    rows = cursor.fetchall()
    cursor.close()

    return [r for r in rows]


if __name__ == "__main__":
    conn = get_db_connection("marine_experiments")
    print(get_experiment(conn))
