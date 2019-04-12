# from data_models import Pokemon, Party
from flask import Flask, render_template, session, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy.orm import relationship

import csv
# from matplotlib import pyplot as plt
# import seaborn as sns

## App and database config
## Used 'main_app.py' file from lecture as a starting point
app = Flask(__name__)
app.debug = True
app.use_reloader = True
app.config['SECRET_KEY'] = 'hard to guess string for app security adgsdfsadfdflsdfsj'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./pokemon_dashboard.db'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# Set up Flask debug stuff
db = SQLAlchemy(app) # For database use
session = db.session # to make queries easy

## Definitely one to drop what's in the DB and load in the pokemon data

## Classes for database models
party_table = Table('party_to_pokemon', Base.metadata,
    Column('party_id', Integer, ForeignKey('party.id')),
    Column('pokemon_id', Integer, ForeignKey('pokemon.id')))

class Pokemon(db.Model):
    __tablename__ = 'pokemon'
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    number = db.Column(db.Integer)
    name = db.Column(db.String(64))
    type_1 = db.Column(db.String(64))
    type_2 = db.Column(db.String(64))
    Total = db.Column(db.Integer)
    HP = db.Column(db.Integer)
    Attack = db.Column(db.Integer)
    Defense = db.Column(db.Integer)
    Sp_Attack = db.Column(db.Integer)
    Sp_Defense = db.Column(db.Integer)
    Speed = db.Column(db.Integer)

class Game(db.Model):
    __tablename__ = 'game'
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String(64))
    generation = db.Column(db.Integer)

class Party(db.Model):
    __tablename__ = 'party'
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    game = db.Column(db.Integer)
    nickname = db.Column(db.String(64))
    party_size = db.Column(db.Integer)

    pokemon = relationship('Pokemon', secondary = party_table, backref = 'parties')

## Route functions
@app.route('/')
def index():
    num_rows = str(Pokemon.query.count())
    return '<h1>There are {} pokemon in the database.</h1>'.format(num_rows)

## Helper functions
def fill_pokemon_data():
    with open('data/Pokemon.csv') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        next(readCSV)
        for row in readCSV:
            next_pokemon = Pokemon(number = row[0], name = row[1], type_1 = row[2], type_2 = row[3], Total = row[4],
                                   HP = row[5], Attack = row[6], Defense = row[7], Sp_Attack = row[8],
                                   Sp_Defense = row[9], Speed = row[10])
            session.add(next_pokemon)
        session.commit()

    with open('data/Games.csv') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        next(readCSV)
        for row in readCSV:
            next_game = Game(name = row[0], generation = row[1])
            session.add(next_game)
        session.commit()

if __name__ == '__main__':
    db.drop_all()
    db.create_all()
    fill_pokemon_data()
    app.run(use_reloader=False)
