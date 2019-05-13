import plotly
import plotly.plotly as py
import plotly.graph_objs as go
import json

from db import db
from app import session
import csv
from data_models import *

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

def create_bar_plot(current_team):

    if len(current_team) < 1:
        return None

    data = []
    for member in current_team:
        x = ['HP', 'Attack', 'Defense', 'Sp. Attack', 'Sp. Defense', 'Speed']
        y = [member.pokemon.HP, member.pokemon.Attack, member.pokemon.Defense,
             member.pokemon.Sp_Attack, member.pokemon.Sp_Defense, member.pokemon.Speed]
        name = member.pokemon.name
        bars = go.Bar(x=x, y=y, name=name)
        data.append(bars)

    graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON

def create_pie_chart(current_team):

    if len(current_team) < 1:
        return None

    labels = []
    values = []
    for member in current_team:
        labels.append(member.pokemon.name)
        values.append(member.pokemon.Total)

    data = go.Pie(labels=labels, values=values)
    pieJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)
    return pieJSON
