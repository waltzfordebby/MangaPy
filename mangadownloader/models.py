from mangadownloader import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


manga_genre = db.Table('manga_genre',
                       db.Column('manga_id', db.Integer, db.ForeignKey(
                           'manga.id'), primary_key=True),
                       db.Column('genre_id', db.Integer, db.ForeignKey(
                           'genre.id'), primary_key=True)
                       )


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False,
                           default='default.jpg')
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"User('{self.username}','{self.email}','{self.image_file}')"


class Manga(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image_url = db.Column(db.String(50), nullable=False, default="Unknown")
    title = db.Column(db.String(30), unique=True, nullable=False)
    japanese_title = db.Column(
        db.String(30), unique=True, nullable=False, default="Unknown")
    type = db.Column(db.String(20), nullable=False, default="Unknown")
    volumes = db.Column(db.Integer, nullable=False, default=0)
    chapters = db.Column(db.Integer, nullable=False, default=0)
    status = db.Column(db.String(20), nullable=False, default="Unknown")
    genres = db.relationship(
        'Genre', secondary=manga_genre, lazy='subquery', backref=db.backref('mangas', lazy=True))
    author_id = db.Column(db.Integer, db.ForeignKey(
        'author.id'), nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey(
        'artist.id'), nullable=False)
    serialization = db.Column(db.Text, nullable=False, default="Unknown")
    summary = db.Column(db.Text, nullable=False, default="Unknown")
    created_on = db.Column(db.DateTime, server_default=db.func.now())
    updated_on = db.Column(
        db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

    def __repr__(self):
        return f"Manga('{self.title}','{self.author_id}','{self.type}')"


class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    manga = db.relationship('Manga', backref="author", lazy=True)
    image_url = db.Column(db.String(50), nullable=False, default="Unknown")
    last_name = db.Column(db.String(30), nullable=False, default="None")
    first_name = db.Column(db.String(30), nullable=False, default="None")
    birth_date = db.Column(db.DateTime, nullable=False, default="Unknown")
    created_on = db.Column(db.DateTime, server_default=db.func.now())
    updated_on = db.Column(
        db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

    def __repr__(self):
        return f"Author('{self.last_name}','{self.first_name}','{self.pen_name}')"


class Artist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    manga = db.relationship('Manga', backref="artist", lazy=True)
    image_url = db.Column(db.String(50), nullable=False, default="Unknown")
    last_name = db.Column(db.String(30), nullable=False, default="None")
    first_name = db.Column(db.String(30), nullable=False, default="None")
    birth_day = db.Column(db.DateTime, nullable=False, default="Unknown")
    created_on = db.Column(db.DateTime, server_default=db.func.now())
    updated_on = db.Column(
        db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

    def __repr__(self):
        return f"Author('{self.last_name}','{self.first_name}','{self.pen_name}')"


class Genre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
