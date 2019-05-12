from db import db

## Classes for database models

## Table to help with many-to-many relationship of pokemon and parties
class PartyMember(db.Model):

    __tablename__ = 'party_member'
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    party_id = db.Column(db.Integer, db.ForeignKey('party.id'))
    pokemon_id = db.Column(db.Integer, db.ForeignKey('pokemon.id'))
    extra_data = db.Column(db.Integer)
    pokemon = db.relationship("Pokemon", back_populates="parties")
    party = db.relationship("Party", back_populates="pokemon")

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

    parties = db.relationship("PartyMember", back_populates="pokemon")

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
    game_name = db.Column(db.String(64), db.ForeignKey('game.name'))
    name = db.Column(db.String(64))
    party_size = db.Column(db.Integer)

    pokemon = db.relationship("PartyMember", back_populates = "party")
    game = db.relationship("Game")
