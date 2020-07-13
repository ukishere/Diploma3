import json
import unittest
from unittest import TestCase
# from unittest.mock import patch
import main

class VkinderTest(TestCase):

    def setUp(self):
        main.new_start()
        self.first_result = []
        self.second_result = []
        with open('vkinder_results.json', 'r') as file:
            self.first_result = json.load(file)
        main.new_start()
        with open('vkinder_results.json', 'r') as file:
            self.second_result = json.load(file)

    def test_of_the_result(self):
        self.assertTrue(bool(len(self.first_result)))
        self.assertTrue(bool(len(self.second_result)))

    def test_for_new_result(self):
        random_victim = self.first_result[0]['Vkid']
        for victim in self.second_result:
            self.assertNotEqual(random_victim, victim['Vkid'])

if __name__ == '__main__':
    unittest.main()
