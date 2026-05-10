from models import db, User, Movie


class DataManager:

    def create_user(self, name):
        try:
            user = User(name=name)
            db.session.add(user)
            db.session.commit()
            return user

        except Exception as e:
            db.session.rollback()
            print("Error in create_user:", str(e))
            return None

    def get_users(self):
        try:
            return User.query.all()

        except Exception as e:
            print("Error in get_users:", str(e))
            return []

    def get_movies(self, user_id):
        try:
            return Movie.query.filter_by(user_id=user_id).all()

        except Exception as e:
            print("Error in get_movies:", str(e))
            return []

    def add_movie(self, movie):
        try:
            db.session.add(movie)
            db.session.commit()
            return movie

        except Exception as e:
            db.session.rollback()
            print("Error in add_movie:", str(e))
            return None

    def update_movie(self, movie_id, new_title):
        try:
            movie = Movie.query.get(movie_id)

            if movie:
                movie.name = new_title
                db.session.commit()

            return movie

        except Exception as e:
            db.session.rollback()
            print("Error in update_movie:", str(e))
            return None

    def delete_movie(self, movie_id):
        try:
            movie = Movie.query.get(movie_id)

            if movie:
                db.session.delete(movie)
                db.session.commit()

            return movie

        except Exception as e:
            db.session.rollback()
            print("Error in delete_movie:", str(e))
            return None