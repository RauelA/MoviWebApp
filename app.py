import os
import requests
from flask import Flask, request, redirect, url_for, render_template
from data_manager import DataManager
from models import db, Movie

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
data_dir = os.path.join(basedir, "data")
os.makedirs(data_dir, exist_ok=True)

app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'data/movies.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

data_manager = DataManager()

OMDB_API_KEY = os.getenv("c0772217")


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@app.route('/')
def index():
    users = data_manager.get_users()
    return render_template('index.html', users=users)


@app.route('/users', methods=['POST'])
def add_user():

    name = request.form.get('name')

    if not name:
        return "Missing user name", 400

    data_manager.create_user(name)

    return redirect(url_for('index'))


@app.route('/users/<int:user_id>/movies', methods=['GET'])
def user_movies(user_id):

    movies = data_manager.get_movies(user_id)

    return render_template('movies.html', movies=movies, user_id=user_id)


@app.route('/users/<int:user_id>/movies', methods=['POST'])
def add_movie(user_id):

    title = request.form.get('title')

    if not title:
        return "Missing movie title", 400

    url = f"http://www.omdbapi.com/?t={title}&apikey={OMDB_API_KEY}"
    response = requests.get(url)
    data = response.json()

    movie_name = data.get("Title") or title
    director = data.get("Director") or "Unknown"
    poster = data.get("Poster") or ""
    year_raw = data.get("Year")

    try:
        year = int(year_raw[:4]) if year_raw and year_raw != "N/A" else 0
    except:
        year = 0

    new_movie = Movie(
        name=movie_name,
        director=director,
        year=year,
        poster_url=poster,
        user_id=user_id
    )

    data_manager.add_movie(new_movie)

    return redirect(url_for('user_movies', user_id=user_id))


@app.route('/users/<int:user_id>/movies/<int:movie_id>/update', methods=['POST'])
def update_movie(user_id, movie_id):

    new_title = request.form.get('title')

    if not new_title:
        return "Missing title", 400

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
