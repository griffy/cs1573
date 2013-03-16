import os
import unittest
from ..feature_parser import FeatureParser

class TestFeatureParser(unittest.TestCase):
	def setUp(self):
		self.feature_parser = FeatureParser(os.path.join(os.getcwd(), 'email_classifier/data/beck-s'))
		
	def test___init__(self):
		pass

	def test__information_gain(self):
		pass

	def test__chi_square(self):
		pass


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestFeatureParser))
    return suite

if __name__ == '__main__':
    unittest.main()
