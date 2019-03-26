from flask import render_template, request, Blueprint
from mangadownloader.main.utils import hotMangaData
main = Blueprint('main', __name__)


@main.route("/")
@main.route("/home")
def home():
    return render_template('main/home.html', title="Home", hotmanga=hotMangaData())


@main.route("/about")
def about():
    return render_template('main/about.html')
