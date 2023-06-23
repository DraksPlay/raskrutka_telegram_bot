import unittest
from . import Nakrutka
import configparser
import os


class MyTestCase(unittest.TestCase):
    def test_something(self):
        config = configparser.ConfigParser()
        config.read("C:/Users/DraksPlay/PycharmProjects/raskrutka/bot/config.ini")
        narkutka = Nakrutka(config["NakrutkaAPI"]["api_key"])
        self.assertEqual(narkutka.order_status(357835), 29.10)  # add assertion here


if __name__ == '__main__':
    unittest.main()
