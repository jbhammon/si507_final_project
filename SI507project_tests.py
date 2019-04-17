import unittest
from SI507project_tools import *

class StepOne(unittest.TestCase):

    def setUp(self):
        ## create class instances the tests below will need
        # self.pokemon = Pokemon.query.filter_by(name = 'butterfree').first()
        # self.party = Party(game = 'Gold', name = 'The OG', party_size = 0)
        # first_party = Party(game = 'Gold', name = 'The OG', party_size = 0)
        # session.add(first_party)
        # session.commit()
        pass

    ## Test number of rows in Pokemon table, should be 800
    def test_Pokemon_table_size(self):
        self.assertEqual(Pokemon.query.count(), 800, "Testing that Pokemon table is the correct size.")

    ## Adding to a team should add row to association table
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

        session.add(test_party)
        session.add(test_pokemon)
        session.add(next_member)
        session.commit()

        self.assertEqual(len(test_party.pokemon), 1, "Testing that we can access a Party's Pokemon with the relationship() attribute from the data model.")

    ## Query the association table directly to verify the data is correct there
    ## TODO: figure out how to actually do this...

    # Adding duplicate should also add row to association table
    def test_add_to_team_duplicate(self):
        test_pokemon = Pokemon.query.filter_by(name = 'butterfree').first()
        test_party = Party.query.filter_by(name = 'The OG').first()
        next_member = PartyMember(extra_data = 50)

        next_member.pokemon = test_pokemon
        test_party.pokemon.append(next_member)

        session.add(test_party)
        session.add(test_pokemon)
        session.add(next_member)
        session.commit()

        self.assertEqual(len(test_party.pokemon), 2, "Testing that duplicates can be added to Parties.")

    # ## Shouldn't be able to add a seventh Pokemon to a Team
    # ## Expected to fail at this point
    # def test_party_max_size(self):
    #     self.party.pokemon.append(self.pokemon)
    #     session.add(self.party)
    #     session.add(self.party)
    #     session.add(self.party)
    #     session.add(self.party)
    #     session.add(self.party) ## Seventh pokemon that shouldn't be added
    #     session.commit()
    #     self.assertEqual(len(self.party.pokemon), 6, "Testing the size of a Party is capped at 6 Pokemon.")

    ## Adding a pokemon that doesn't exist

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
