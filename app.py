import requests
from flask import Flask, request, redirect, url_for, render_template
from data_manager import DataManager
from models import db, Movie
import os


OMDB_API_KEY = os.getenv("c0772217")

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
data_dir = os.path.join(basedir, "data")

app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'data/movies.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

data_manager = DataManager()


@app.route('/')
def index():
    users = data_manager.get_users()
    return render_template('index.html', users=users)


@app.route('/users')
def list_users():
    users = data_manager.get_users()
    return str(users)


@app.route('/users', methods=['POST'])
def add_user():
    name = request.form.get('name')
    data_manager.create_user(name)
    return redirect(url_for('home'))


@app.route('/users/<int:user_id>/movies')
def user_movies(user_id):
    movies = data_manager.get_movies(user_id)
    return str(movies)


@app.route('/users/<int:user_id>/movies', methods=['POST'])
def add_movie(user_id):

    title = request.form.get('title')

    response = requests.get(f"http://www.omdbapi.com/?t={title}&apikey={OMDB_API_KEY}")

    data = response.json()

    new_movie = Movie(
        name=data.get("Title"),
        director=data.get("Director"),
        year=int(data.get("Year", 0)[:4]) if data.get("Year") else 0,
        poster_url=data.get("Poster"),
        user_id=user_id
    )

    data_manager.add_movie(new_movie)

    return redirect(url_for('user_movies', user_id=user_id))


@app.route('/users/<int:user_id>/movies/<int:movie_id>/update', methods=['POST'])
def update_movie(user_id, movie_id):
    new_title = request.form.get('title')

    data_manager.update_movie(movie_id, new_title)

    return redirect(url_for('user_movies', user_id=user_id))


@app.route('/users/<int:user_id>/movies/<int:movie_id>/delete', methods=['POST'])
def delete_movie(user_id, movie_id):
    data_manager.delete_movie(movie_id)

    return redirect(url_for('user_movies', user_id=user_id))


def main():
    with app.app_context():
        db.create_all()
    app.run(debug=True)


if __name__ == "__main__":
    main()
