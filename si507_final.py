# from data_models import Pokemon, Party
from flask import Flask, render_template, session, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy

import csv
from matplotlib import pyplot as plt
import seaborn as sns

## App and database config
## Used 'main_app.py' file from lecture as a starting point
app = Flask(__name__)
app.debug = True
app.use_reloader = True
app.config['SECRET_KEY'] = 'hard to guess string for app security adgsdfsadfdflsdfsj'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./my_fav_movies.db'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# Set up Flask debug stuff
db = SQLAlchemy(app) # For database use
session = db.session # to make queries easy

## Helper functions

## Definitely one to drop what's in the DB and load in the pokemon data

## Classes for database models

## Route functions

if __name__ == '__main__':
    db.create_all()
    ## Helper function to initialize db
    app.run()
