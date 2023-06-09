# Original from https://github.com/pallets/flask/blob/main/examples/tutorial/flaskr/db.py
import sqlite3
from flask import current_app
from flask import g
from flask.cli import with_appcontext
import os


def get_db():
    """Connect to the application's configured database. The connection
    is unique for each request and will be reused if this is called again.
    """
    if "db" not in g:
        g.db = sqlite3.connect(
            current_app.config["DATABASE"], detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
    return g.db


def close_db(e=None):
    """If this request connected to the database, close the
    connection.
    """
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    """Clear existing data and create new tables."""

    # check if the database file is exist
    if not os.path.isfile(current_app.config["DATABASE"]):
        db = get_db()
        with current_app.open_resource("schema.sql") as f:
            db.executescript(f.read().decode("utf8"))


def init_app(app):
    """Register database functions with the Flask app. This is called by
    the application factory.
    """
    app.teardown_appcontext(close_db)
