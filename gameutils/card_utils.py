"""
CS 5001
Rohith Kumar Senthil Kumar
Fall 2024

funtions on card utilities
"""

import random

def compare_cards(card_a, card_b):
    """compare_cards: compares if two Card classes are the same, returns a bool
    based on the result

    Args:
        card_a (Card): Card class - previous or active chosen card
        card_b (Card): Card class - currently chosen card

    Returns:
        bool: True if they are the same cards
    """
    
    return card_a.name == card_b.name and card_a.index != card_b.index

def calculate_score(total_cards, total_clicks):
    """calculate_score: Calculates the final score of the player based on the
    number of clicks

    Args:
        total_cards (int): total number of cards
        total_clicks (int): total clicks to win the game

    Returns:
        int: score
    """
    
    return round(100*(total_cards/total_clicks))

def three_cards_clicked_at_once(card_handler_dict, active_card_index):
    """three_cards_clicked_at_once: returns Tru if three cards are selected
    back to back which the first 2 cards are still being processed. This is to 
    limit clicks to 2 per card selection session.

    Args:
        card_handler_dict (_type_): main gameplay details dictionary
        active_card_index (_type_): index of the previously clicked card
        
    Returns:
        bool: True if 3 cards are clicked back to back
    """
    
    return card_handler_dict['click_count']!=1 and card_handler_dict[
        'click_count'] %2 !=0 and active_card_index != None
    
def initialize_card_handler():
    return {'active_card_index' : None,'click_count' : 0, 'right_choices' : 0, 
    'cards': [] }

def reset_turtle(turtles):
    """reset_turtle: resets a list of turtle passed to it, and hides them 
    individually

    Args:
        turtles (list): turtle instances list
    """
    
    for turtle_ in turtles:
        turtle_.reset()
        turtle_.hideturtle()

def prepare_cards(cards_count, cards_list):
    """prepare_cards: truncates the cards_list to the cards count inputed by 
    the  user or player. If the card deck has 20 cards, will return only the
    number of cards equal to cards_count, and shuffles the list

    Args:
        cards_count (_type_): user input
        cards_list (_type_): list of card paths from the assets

    Returns:
        list: cards_list with length of cards_count
    """
    
    cards_list = cards_list[:int(cards_count) // 2]
    cards_list = cards_list + cards_list
    random.shuffle(cards_list)
    return cards_list

def is_card_count_odd(cards_count):
    """is_card_count_odd: checks if the cards_count is odd

    Args:
        cards_count (_type_): user input

    Returns:
        bool: True if odd count
    """
    
    return int(cards_count) != 1 and int(cards_count) % 2 != 0
    
def is_card_count_valid(cards_count, cards_list):
    """is_card_count_valid: checks if the cards_count given by the user is even
    and is greater than 7 and if the chosen card deck has enough cards to play
    with 

    Args:
        cards_count (_type_): user input
        cards_list (_type_): list  of card path from the card deck

    Returns:
        bool: True if the cards_count given by the user is even
    and is greater than 7 and if the chosen card deck has enough cards to play
    with 
    """
    
    return int(cards_count) % 2 == 0 and int(cards_count) > 7 and \
        len(cards_list)*2 >= int(cards_count)