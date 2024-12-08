"""
CS 5001
Rohith Kumar Senthil Kumar
Fall 2024

A PyUnint test class for a class to test the game utils
"""

import unittest
import os
import turtle
from gameutils import menu_screen_utils
from gameutils import card_utils
from model.card import Card

class TestGameUtils(unittest.TestCase):
    
    def test_compare_cards(self):
        """tests compare_cards from the card_utils
        """
        
        turtle.Screen().register_shape(os.path.join(os.path.join(
            os.getcwd(), 'assets'), 'card_back.gif'))
        self.assertTrue(card_utils.compare_cards(Card(
            1, 'test'), Card(2, 'test')))
        self.assertFalse(card_utils.compare_cards(Card(1, 'test'), Card(
            1, 'test')))
        
    def  test_calculate_score(self):
        """tests calculate_score from the card_utils
        """
        
        self.assertEqual(card_utils.calculate_score(8, 8), 100)
        
    def  test_initialize_card_handler(self):
        """tests initialize_card_handler from the card_utils
        """
        
        test_dict = {'active_card_index' : None,'click_count' : 0, 
                     'right_choices' : 0, 'cards': [] }
        self.assertEqual(card_utils.initialize_card_handler(), test_dict)
        
    def test_is_card_count_odd(self):
        """tests is_card_count_odd from the card_utils
        """
        
        self.assertTrue(card_utils.is_card_count_odd(7))
    
    def test_is_card_count_valid(self):
        """tests is_card_count_odd from the card_utils
        """

        self.assertFalse(card_utils.is_card_count_valid(85, [0]*12))
        
    def test_is_valid_asset_folder(self):
        """tests is_valid_asset_folder from the menu_screen_utils
        """
        
        for asset in os.listdir(os.path.join(os.getcwd(), 'assets')):
            if '.' in asset:
                continue 
            asset_path = os.path.join(os.path.join(os.getcwd(), 'assets'), 
                                      asset)
            self.assertTrue(menu_screen_utils.is_valid_asset_folder(
                asset_path))

        self.assertFalse(menu_screen_utils.is_valid_asset_folder(
                'dummy_path'))
        
    def test_load_cards_from_card_deck(self):
        """tests load_cards_from_card_deck from the menu_screen_utils
        """

        for asset in os.listdir(os.path.join(os.getcwd(), 'assets')):
            if '.' in asset:
                continue 
            asset_path = os.path.join(os.path.join(os.getcwd(), 'assets'), 
                                      asset)
            self.assertNotEqual(len(
                menu_screen_utils.load_cards_from_card_deck(asset_path)), 0)
            break
        with self.assertRaises(FileNotFoundError):
            menu_screen_utils.load_cards_from_card_deck('dummy_path')
    
    def test_load_menu_screen(self):
        """tests load_menu_screen from the menu_screen_utils
        """
        
        self.assertNotEqual(menu_screen_utils.load_menu_screen_data(), {})
        
def main():
    unittest.main(verbosity=3)

if  __name__ == '__main__':
    main() 
    