from flask import Flask, request, render_template, redirect, url_for
from db import db
from data_models import PartyMember, Pokemon, Game, Party
from tools import *

## App and database config
## Used 'main_app.py' file from lecture as a starting point
app = Flask(__name__)
app.debug = True
app.use_reloader = True
app.config['SECRET_KEY'] = 'hard to guess string for app security adgsdfsadfdflsdfsj'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./pokemon_dashboard.db'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

session = db.session

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

    # stats_dict = {'stat': [], 'value': []}
    current_party = Party.query.filter_by(name = teamname).first()
    current_team = current_party.pokemon
    current_team_names = []
    for member in current_team:
        current_team_names.append(member.pokemon.name)

        ## Collecting data about the party's current stats
        ## This will get aggregated and plotted below
        # stats_dict['stat'].append('HP')
        # stats_dict['value'].append(member.pokemon.HP)
        #
        # stats_dict['stat'].append('Attack')
        # stats_dict['value'].append(member.pokemon.Attack)
        #
        # stats_dict['stat'].append('Defense')
        # stats_dict['value'].append(member.pokemon.Defense)
        #
        # stats_dict['stat'].append('Sp. Attack')
        # stats_dict['value'].append(member.pokemon.Sp_Attack)
        #
        # stats_dict['stat'].append('Sp. Defense')
        # stats_dict['value'].append(member.pokemon.Sp_Defense)
        #
        # stats_dict['stat'].append('Speed')
        # stats_dict['value'].append(member.pokemon.Speed)

    # if len(current_team) > 0:
    #     ## Convert that stats dictionary to a pandas DataFrame object
    #     df_stats = pd.DataFrame.from_dict(stats_dict)
    #
    #     ## Plotting a bar plot with Seaborn of a sum each stat for the whole party
    #     fig = sns.barplot(x = "stat", y = "value", data = df_stats, estimator = sum,
    #                       ci = None).get_figure()
    #     fig.savefig("static/team_stats_barplot.png", dpi=300)

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

if __name__ == '__main__':
    app.run()
