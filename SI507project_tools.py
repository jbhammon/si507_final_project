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

RESISTANCES = {'Normal': ['Ghost'],
               'Fighting': ['Rock', 'Bug', 'Dark'],
               'Flying': ['Fighting', 'Ground', 'Bug', 'Grass'],
               'Poison': ['Fighting', 'Poison', 'Bug', 'Grass', 'Fairy'],
               'Ground': ['Poison', 'Rock'],
               'Rock': ['Normal', 'Flying', 'Poison', 'Fire'],
               'Bug': ['Fighting', 'Ground', 'Grass'],
               'Ghost': ['Normal', 'Fighting', 'Poison', 'Bug'],
               'Steel': ['Normal', 'Flying', 'Poison', 'Rock', 'Bug', 'Steel', 'Grass', 'Psychic', 'Ice', 'Dragon', 'Fairy'],
               'Fire': ['Bug', 'Steel', 'Fire', 'Grass', 'Ice', 'Fairy'],
               'Water': ['Steel', 'Fire', 'Water', 'Ice'],
               'Grass': ['Ground', 'Water', 'Grass', 'Electric'],
               'Electric': ['Flying', 'Steel', 'Electric'],
               'Psychic': ['Fighting', 'Psychic'],
               'Ice': ['Ice'],
               'Dragon': ['Fire', 'Water', 'Grass', 'Electric'],
               'Dark': ['Ghost', 'Psychic', 'Dark'],
               'Fairy': ['Fighting', 'Bug', 'Dark']}

## Classes for database models

## Table to help with many-to-many relationship of pokemon and parties
class PartyMember(db.Model):

    __tablename__ = 'party_member'
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    party_id = Column(db.Integer, ForeignKey('party.id'))
    pokemon_id = Column(db.Integer, ForeignKey('pokemon.id'))
    extra_data = Column(db.Integer)
    pokemon = relationship("Pokemon", back_populates="parties")
    party = relationship("Party", back_populates="pokemon")

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
    Generation = db.Column(db.Integer)

    parties = relationship("PartyMember", back_populates="pokemon")

    def details(self):
        data = [self.name, self.type_1, self.type_2, self.Total, self.Attack, self.Defense,
                self.Sp_Attack, self.Sp_Defense, self.Speed, self.HP]
        return data

class Game(db.Model):
    __tablename__ = 'game'
    # id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String(64), primary_key = True)
    generation = db.Column(db.Integer)

class Party(db.Model):
    __tablename__ = 'party'
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    game_name = db.Column(db.String(64), ForeignKey('game.name'))
    name = db.Column(db.String(64))
    party_size = db.Column(db.Integer)

    pokemon = relationship("PartyMember", back_populates = "party")
    game = relationship("Game")

## Route functions
@app.route('/', methods = ['POST', 'GET'])
def index():
    if request.method == 'POST':
        game = request.form['game']
        name = request.form['name']
        player_game = Game.query.filter_by(name = game).first()
        new_party = Party(game = player_game, name = name, party_size = 0)
        session.add(new_party)
        session.commit()

    recent_three_teams = Party.query.order_by(Party.id.desc()).limit(3).all()
    recent_three_strings = []
    for team in recent_three_teams:
        recent_three_strings.append(str(team.name))

    game_names = [r.name for r in Game.query.with_entities(Game.name)]

    return render_template('index.html', recent_teams = recent_three_strings,
                           game_names = game_names)

@app.route('/build_team/<teamname>', methods = ['POST', 'GET'])
def build_team(teamname):
    error = None
    if request.method == 'POST':

        party = Party.query.filter_by(name = teamname).first()
        next_pokemon = Pokemon.query.filter_by(name = request.form['name'].lower()).first()
        if(next_pokemon):
            if(next_pokemon.Generation <= party.game.generation):
                next_member = PartyMember(extra_data = 50)
                next_member.pokemon = next_pokemon
                party.pokemon.append(next_member)
                party.party_size += 1

                session.add(party)
                session.add(next_pokemon)
                session.add(next_member)
                session.commit()
            else:
                error = "Error: That Pokemon isn't available in {}".format(party.game.name)
        else:
            error = "Error: That pokemon doesn't exist in the database. Make sure you spelled its name right!"

    current_party = Party.query.filter_by(name = teamname).first()
    current_team = current_party.pokemon
    current_team_names = []
    for member in current_team:
        current_team_names.append(member.pokemon.name)

    ## code to calculate missing type coverage
    resistances = resistance_checking(current_team)
    missing_resistances = []
    for poke_type in resistances:
        if resistances[poke_type] == 0:
            missing_resistances.append(poke_type)

    return render_template('view_team.html', team_members = current_team_names,
                           missing_resistances = missing_resistances, teamname = teamname,
                           teamsize = current_party.party_size, error = error)

@app.route('/delete/<teamname>/<pokemon>')
def delete_from_team(teamname, pokemon):
    ## deleting pokemon from the party
    current_party = Party.query.filter_by(name = teamname).first()
    current_team = current_party.pokemon
    for member in current_team:
        if(member.pokemon.name == pokemon):
            session.delete(member)
            current_party.party_size -= 1
            break

    return redirect(url_for('build_team', teamname = teamname))

@app.route('/details/<pokemon>')
def pokemon_details(pokemon):
    subject = Pokemon.query.filter_by(name = pokemon.lower()).first()
    return render_template('pokemon.html', subject = subject.details())

@app.route('/db_refresh')
def database_refresh():
    db.drop_all()
    db.create_all()
    fill_pokemon_data()
    return render_template('refresh.html')

## Helper functions
def fill_pokemon_data():
    with open('data/Pokemon.csv') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        next(readCSV)
        for row in readCSV:
            next_pokemon = Pokemon(number = row[0], name = row[1].lower(), type_1 = row[2], type_2 = row[3], Total = row[4],
                                   HP = row[5], Attack = row[6], Defense = row[7], Sp_Attack = row[8],
                                   Sp_Defense = row[9], Speed = row[10], Generation = row[11])
            session.add(next_pokemon)
        session.commit()

    with open('data/Games.csv') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        next(readCSV)
        for row in readCSV:
            next_game = Game(name = row[0], generation = row[1])
            session.add(next_game)
        session.commit()

## Function to help check a party's pokemon's types and find the weaknesses that aren't covered
def resistance_checking(team):
    resistance_dict = {'Normal': 0,
                       'Fighting': 0,
                       'Flying': 0,
                       'Poison': 0,
                       'Ground': 0,
                       'Rock': 0,
                       'Bug': 0,
                       'Ghost': 0,
                       'Steel': 0,
                       'Fire': 0,
                       'Water': 0,
                       'Grass': 0,
                       'Electric': 0,
                       'Psychic': 0,
                       'Ice': 0,
                       'Dragon': 0,
                       'Dark': 0,
                       'Fairy': 0}

    for member in team:
        resistances = RESISTANCES[member.pokemon.type_1]
        if(member.pokemon.type_2):
            resistances = resistances + RESISTANCES[member.pokemon.type_2]
        for item in resistances:
            resistance_dict[item] = 1
    return resistance_dict

if __name__ == '__main__':
    app.run()
