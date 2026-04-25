from pathlib import Path
import sqlite3

from flask import Flask
from models import db
from routes import main

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///workout.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


def ensure_schema_loaded(flask_app):
    db_path = Path(flask_app.instance_path) / "workout.db"
    schema_path = Path(flask_app.root_path) / "schema.sql"

    db_path.parent.mkdir(parents=True, exist_ok=True)

    with sqlite3.connect(db_path) as connection:
        existing_tables = {
            row[0]
            for row in connection.execute(
                "SELECT name FROM sqlite_master WHERE type='table'"
            )
        }

        if "Users" in existing_tables:
            return

        connection.executescript(schema_path.read_text(encoding="utf-8"))
        connection.commit()

db.init_app(app)
app.register_blueprint(main)

with app.app_context():
    ensure_schema_loaded(app)

import routes
print("APP STARTED")

if __name__ == "__main__":
    app.run(debug=True)
