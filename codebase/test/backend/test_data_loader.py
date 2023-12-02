import unittest
import sys

sys.append("../../src/backend")
from data_loader import DataLoader

class TestDataLoader(unittest.TestCase):
    def test_(self): 
        pass
            


# Execute Test Runner
suite = unittest.TestLoader().loadTestsFromTestCase(TestDataLoader)
_ = unittest.TextTestRunner().run(suite)