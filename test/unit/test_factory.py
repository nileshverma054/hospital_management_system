import unittest
from src.api import app


class TestFactory(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = app.test_client()

    @classmethod
    def tearDownClass(cls):
        pass
