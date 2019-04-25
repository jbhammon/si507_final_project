import unittest
from SI507project_tools import *

class StepOne(unittest.TestCase):

    def setUp(self):
        pass

    ## Test number of rows in Pokemon table after a DB refresh, should be 800
    def test_Pokemon_table_size(self):
        db.drop_all()
        db.create_all()
        fill_pokemon_data()
        self.assertEqual(Pokemon.query.count(), 800, "Testing that Pokemon table is the correct size.")

    ## testing that logic to add pokemon to parties is correct
    def test_add_to_team(self):

        first_party = Party(game = 'Gold', name = 'The OG', party_size = 0)
        session.add(first_party)
        session.commit()

        test_pokemon = Pokemon.query.filter_by(name = 'butterfree').first()
        test_party = Party.query.filter_by(name = 'The OG').first()
        self.assertEqual(len(test_party.pokemon), 0, "Testing that association table is the correct size.")
        next_member = PartyMember(extra_data = 50)
        next_member.pokemon = test_pokemon
        test_party.pokemon.append(next_member)
        test_party.party_size += 1

        session.add(test_party)
        session.add(test_pokemon)
        session.add(next_member)
        session.commit()

        self.assertEqual(len(test_party.pokemon), 1, "Testing that we can access a Party's Pokemon with the relationship() attribute from the data model.")

    # Adding duplicate should also add row to association table
    def test_add_to_team_duplicate(self):
        test_pokemon = Pokemon.query.filter_by(name = 'butterfree').first()
        test_party = Party.query.filter_by(name = 'The OG').first()
        next_member = PartyMember(extra_data = 50)

        next_member.pokemon = test_pokemon
        test_party.pokemon.append(next_member)
        test_party.party_size += 1

        session.add(test_party)
        session.add(test_pokemon)
        session.add(next_member)
        session.commit()

        self.assertEqual(len(test_party.pokemon), 2, "Testing that duplicates can be added to Parties.")

    ## Should be able to add a seventh Pokemon to a Team
    ## Users will be prevented from adding more than 6 Pokemon in the Flask template
    def test_party_max_size(self):
        test_pokemon = Pokemon.query.filter_by(name = 'butterfree').first()
        test_party = Party.query.filter_by(name = 'The OG').first()

        next_member = PartyMember(extra_data = 50)
        next_member.pokemon = test_pokemon
        test_party.pokemon.append(next_member)
        test_party.party_size += 1
        session.add(next_member)

        next_member = PartyMember(extra_data = 50)
        next_member.pokemon = test_pokemon
        test_party.pokemon.append(next_member)
        test_party.party_size += 1
        session.add(next_member)

        next_member = PartyMember(extra_data = 50)
        next_member.pokemon = test_pokemon
        test_party.pokemon.append(next_member)
        test_party.party_size += 1
        session.add(next_member)

        next_member = PartyMember(extra_data = 50)
        next_member.pokemon = test_pokemon
        test_party.pokemon.append(next_member)
        test_party.party_size += 1
        session.add(next_member)

        next_member = PartyMember(extra_data = 50)
        next_member.pokemon = test_pokemon
        test_party.pokemon.append(next_member)
        test_party.party_size += 1
        session.add(next_member)

        session.add(test_pokemon)
        session.add(next_member)
        session.commit()
        self.assertEqual(len(test_party.pokemon), 7, "Testing that we can add 7 Pokemon to a party.")

    def test_party_size(self):
        test_party = Party.query.filter_by(name = 'The OG').first()
        self.assertEqual(test_party.party_size, 7, "Testing that the party size is incrementing in the database correctly.")

    def test_resistance_helper(self):
        test_party = Party.query.filter_by(name = 'The OG').first().pokemon
        test_dict = {'Normal': 0,
                     'Fighting': 1,
                     'Flying': 0,
                     'Poison': 0,
                     'Ground': 1,
                     'Rock': 0,
                     'Bug': 1,
                     'Ghost': 0,
                     'Steel': 0,
                     'Fire': 0,
                     'Water': 0,
                     'Grass': 1,
                     'Electric': 0,
                     'Psychic': 0,
                     'Ice': 0,
                     'Dragon': 0,
                     'Dark': 0,
                     'Fairy': 0}
        results = resistance_checking(test_party)
        self.assertEqual(test_dict, results, "Testing that the correct resistances for a party are returned.")

    def tearDown(self):
        ## delete all the classes we created in setUp()
        # del(self.pokemon)
        # del(self.party)
        pass

if __name__ == "__main__":
    db.drop_all()
    db.create_all()
    fill_pokemon_data()
    unittest.main(verbosity = 2)
