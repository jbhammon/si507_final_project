import unittest
from SI507project_tools import *

class StepOne(unittest.TestCase):

    def setUp(self):
        ## create class instances the tests below will need
        pass

	# def test_subclasses_instance_of_currency(self):
    #
	# 	self.assertIsInstance(self.dollar, Currency,"Testing that an instance of Dollar is an instance of a subclass of Currency")

    def tearDown(self):
        ## delete all the classes we created in setUp()
        # del(self.dollar)
        pass

if __name__ == "__main__":
    unittest.main(verbosity = 2)
