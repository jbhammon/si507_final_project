# from data_models import Pokemon, Party
from flask import Flask, render_template, session, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Table, Column, ForeignKey, Integer, String, Boolean
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
party_table = db.Table('party_to_pokemon',
    db.Column('party_id', db.Integer, db.ForeignKey('party.id')),
    db.Column('pokemon_id', db.Integer, db.ForeignKey('pokemon.id')))

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

    def details(self):
        data = [self.name, self.type_1, self.type_2, self.Total, self.Attack, self.Defense,
                self.Sp_Attack, self.Sp_Defense, self.Speed, self.HP]
        return data

class Game(db.Model):
    __tablename__ = 'game'
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String(64))
    generation = db.Column(db.Integer)

class Party(db.Model):
    __tablename__ = 'party'
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    game = db.Column(db.Integer)
    name = db.Column(db.String(64))
    party_size = db.Column(db.Integer)

    pokemon = relationship('Pokemon', secondary = party_table, backref = 'parties')

## Route functions
@app.route('/', methods = ['POST', 'GET'])
def index():
    if request.method == 'POST':
        game = request.form['game']
        name = request.form['name']
        new_party = Party(game = game, name = name, party_size = 0)
        session.add(new_party)
        session.commit()

    recent_three_teams = Party.query.order_by(Party.id.desc()).limit(3).all()
    recent_three_strings = []
    for team in recent_three_teams:
        recent_three_strings.append(str(team.name))

    return render_template('index.html', recent_teams = recent_three_strings)

@app.route('/build_team/<teamname>', methods = ['POST', 'GET'])
def build_team(teamname):
    if request.method == 'POST':
        ## find
        party = Party.query.filter_by(name = teamname).first()
        next_pokemon = Pokemon.query.filter_by(name = request.form['name'].lower()).first()
        party.pokemon.append(next_pokemon)
        session.add(party)
        session.commit()

    current_team = Party.query.filter_by(name = teamname).first().pokemon
    current_team_names = []
    for pokemon in current_team:
        current_team_names.append(pokemon.name)

    return render_template('view_team.html', team_members = current_team_names)

@app.route('/details/<pokemon>')
def pokemon_details(pokemon):
    subject = Pokemon.query.filter_by(name = pokemon.lower()).first()
    return render_template('pokemon.html', subject = subject.details())

## Helper functions
def fill_pokemon_data():
    with open('data/Pokemon.csv') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        next(readCSV)
        for row in readCSV:
            next_pokemon = Pokemon(number = row[0], name = row[1].lower(), type_1 = row[2], type_2 = row[3], Total = row[4],
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
