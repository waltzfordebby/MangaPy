from flask import render_template, request, Blueprint

malscraper = Blueprint('malscraper', __name__)


@malscraper.route("/malscraper_home")
def malscraper_home():
    return render_template('malscraper/malscraper.html')
