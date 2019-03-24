import os


class Config:
    SECRET_KEY = 'ff5d433d601b7f207e5a0d7c93b169f9'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://waltzfordebby:password@localhost/mangadownloader'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
