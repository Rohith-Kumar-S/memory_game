
import random

def compare_cards(card_a, card_b):
    return card_a.name == card_b.name and card_a.index != card_b.index

def calculate_score(total_cards, total_clicks):
    return round(100*(total_cards/total_clicks))

def three_cards_clicked_at_once(card_handler_dict, active_card_index):
    return card_handler_dict['click_count']!=1 and card_handler_dict[
        'click_count'] %2 !=0 and active_card_index != None
    
def initialize_card_handler():
    return {'active_card_index' : None,'click_count' : 0, 'right_choices' : 0, 
    'cards': [] }

def reset_turtle(turtles):
    for turtle_ in turtles:
        turtle_.reset()
        turtle_.hideturtle()

def prepare_cards(cards_count, cards_list):
    cards_list = cards_list[:int(cards_count)//2]
    cards_list = cards_list+cards_list
    random.shuffle(cards_list)
    return cards_list

def is_card_count_odd(cards_count):
    return int(cards_count) != 1 and int(cards_count) % 2 != 0
    
def is_card_count_valid(cards_count, cards_list):
    return int(cards_count) % 2 == 0 and int(cards_count) > 7 and \
        len(cards_list)*2 >= int(cards_count)