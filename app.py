from flask import Flask
from models import db
from routes import main

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///workoutDatabase.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
app.register_blueprint(main)

import routes
print("APP STARTED")

if __name__ == "__main__":
    app.run(debug=True)