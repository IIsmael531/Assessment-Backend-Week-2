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


conn = get_db_connection("marine_experiments")


def get_cursor(conn: connection) -> cursor:
    """Returns a cursor object using the provided database connection."""
    return conn.cursor()


def get_subject():
    """Returns all subject details"""
    cursor = get_cursor(conn)

    query = """SELECT subject_id, subject_name, species_name, date_of_birth
    FROM subject 
    JOIN species USING(species_id)
    ORDER BY date_of_birth DESC"""

    cursor.execute(query,)
    rows = cursor.fetchall()
    cursor.close()

    return [r for r in rows]


if __name__ == "__main__":
    print(get_subject())
