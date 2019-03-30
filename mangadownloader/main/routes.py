from flask import render_template, request, Blueprint
from mangadownloader.main.utils import hot_manga_data, popular_manga_data, todays_manga_data, yesterdays_manga_data, older_manga_data
main = Blueprint('main', __name__)


@main.route("/")
@main.route("/home")
def home():
    return render_template('main/home.html', title="Home", hot_manga=hot_manga_data(), popular_manga=popular_manga_data(), todays_manga=todays_manga_data(), yestedays_manga=yesterdays_manga_data(), older_manga=older_manga_data())


@main.route("/about")
def about():
    return render_template('main/about.html')
