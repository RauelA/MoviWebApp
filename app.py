from flask import Flask
from models import db, Movie
from data_manager import DataManager

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movies.db'

db.init_app(app)

data_manager = DataManager()

@app.route("/")
def home():
    return "Hello Flask"


@app.route("/add_movie")
def add_movie():

    new_movie = Movie(
        name="Interstellar",
        director="Christopher Nolan",
        year=2014,
        poster_url="https://...",
        user_id=1
    )

    data_manager.add_movie(new_movie)

    return "Movie added successfully!"


def main():
    with app.app_context():
        db.create_all()
    app.run(debug=True)


if __name__ == "__main__":
    main()
