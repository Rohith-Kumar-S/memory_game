"""
CS 5001
Rohith Kumar Senthil Kumar
Project
"""

import turtle
from model.card import Card
import time
from gameutils import menu_screen_utils
from gameutils import card_utils
from gameutils import draw_utils
from gameutils import data_management_utils

def end_game(cards, card_handler_dict, players_dict, score_turtles, end_popup):
    players_dict[list(players_dict.keys())[-1]]["score"] = \
        card_utils.calculate_score(len(cards), card_handler_dict['click_count'
                                                                 ])
    players_dict[list(players_dict.keys())[-1]]["clicks"] = \
        card_handler_dict['click_count']
    player_key = list(players_dict.keys())[-1]
    players_dict = dict(
        sorted(players_dict.items(), key=lambda item: item[1]['clicks']))
    
    if len(players_dict) == 11:
        if list(players_dict.keys())[-1] == player_key:
            end_popup.showturtle()
            return
        else:
            key_to_be_deleted = list(players_dict.keys())[-1]
            del players_dict[key_to_be_deleted]
            
    draw_utils.load_score_board(players_dict, score_turtles)
    data_management_utils.save_leaderboard_details(players_dict)
    end_popup.showturtle()
    
def process_card_actions(cards, active_card_index, current_card_index, 
                         card_handler_dict, action_turtles, column_value):
    if card_utils.compare_cards(
        cards[active_card_index], cards[current_card_index]):
        time.sleep(1)
        cards[active_card_index].hide_card()
        cards[current_card_index].hide_card()
        card_handler_dict['right_choices'] += 1
    else:
        time.sleep(1)
        cards[active_card_index].reset_card()
        cards[current_card_index].reset_card()
        
    card_handler_dict['active_card_index'] = None
    draw_utils.load_player_action_details(
        card_handler_dict, action_turtles, column_value)    

def card_clicked(card_handler_dict, players_dict, current_card_index, 
                   score_turtles, action_turtles, column_value, end_popup):
    cards = card_handler_dict['cards']
    active_card_index = card_handler_dict['active_card_index']
    card_handler_dict['click_count'] += 1
    
    # restrict clicks to 2 per check
    if card_utils.three_cards_clicked_at_once(
        card_handler_dict, active_card_index):
        card_handler_dict['click_count'] -= 1
        return
        
    cards[current_card_index].flip_card()
    
    if active_card_index != None:
        process_card_actions(cards, active_card_index, current_card_index, 
                         card_handler_dict, action_turtles, column_value)
    else:
        card_handler_dict['active_card_index'] = current_card_index
        
    if card_handler_dict['right_choices'] == len(cards)//2:
        end_game(cards, card_handler_dict, players_dict, score_turtles, 
                 end_popup)
        
def draw_and_play_cards(cards_list, card_handler_dict, players_dict, 
                        score_turtles, action_turtles, column_value, 
                        end_popup):
    try:
        for i, path in enumerate(cards_list):
            card_handler_dict['cards'].append(Card(index=i, name=path))
            card_handler_dict['cards'][i].turtle.onclick(
                lambda x , y, turtle_index = i : card_clicked(
                    card_handler_dict, players_dict, turtle_index, score_turtles, 
                    action_turtles, column_value, end_popup))
    except Exception:
        print('something went wrong in draw_and_play_cards')

def handle_in_game_quit_button(end_popup, quit_message, quit_button, 
                               score_turtles, action_turtles, start_btn, 
                               card_handler_dict):
    end_popup.hideturtle()
    quit_message.showturtle()
    
    for card in card_handler_dict['cards']:
        card.turtle.hideturtle()
        
    card_utils.reset_turtle(score_turtles)
    card_utils.reset_turtle(action_turtles)
    quit_button.hideturtle()
    time.sleep(2)
    quit_message.hideturtle()
    draw_utils.get_game_title(start_btn)
    start_btn.showturtle()
    card_handler_dict = card_utils.initialize_card_handler()

def start_game(cards_list, players_dict, score_turtles, column_value):
    try:
        card_handler_dict = card_utils.initialize_card_handler()
        action_turtles = draw_utils.load_player_action_details(
            card_handler_dict, [], column_value)
        end_popup = draw_utils.load_pop_up('winner.gif')
        draw_and_play_cards(cards_list, card_handler_dict, players_dict, 
          score_turtles, action_turtles, column_value, end_popup)
        quit_button = draw_utils.load_quit_button()
        start_btn = draw_utils.load_start_button()
        quit_message = draw_utils.load_pop_up('quitmsg.gif')
        
        def handle_quit_button(x,y):
            nonlocal card_handler_dict
            handle_in_game_quit_button(end_popup, quit_message, quit_button, 
                               score_turtles, action_turtles, start_btn, 
                               card_handler_dict)
        
        def handle_start_button(x,y):
            start_btn.hideturtle()
            start_btn.clear()
            load_card_selection_menu()
            
        start_btn.onclick(handle_start_button)    
        quit_button.onclick(handle_quit_button)
    except Exception:
        print('start_game: something went wrong')
    
def process_cards_and_start_game(cards_list, cards_count, player_name):
    if card_utils.is_card_count_odd(cards_count):
        warning_popup = draw_utils.load_pop_up('card_warning.gif')
        warning_popup.showturtle()
        time.sleep(3)
        warning_popup.hideturtle()
        cards_count = int(cards_count) - 1
        
    if card_utils.is_card_count_valid(cards_count, cards_list):
        players_dict, cards_list, score_turtles, column_value = \
        data_management_utils.process_game_parameters(
            player_name, cards_list, cards_count)
        start_game(cards_list, players_dict, score_turtles, column_value)
    else:
        cards_count = 0
        
    return cards_count
    
def request_details_and_start_game():
    screen = turtle.Screen()
    player_name = None
    cards_count = 0
    cards_list = data_management_utils.load_cards(screen)
    
    while player_name == None:
        player_name = screen.textinput("Welcome to the Memory Game!", \
"Enter your name")
        if player_name is None:
            return False
        elif player_name.strip() == '':
            continue
        
        while cards_count == 0:
            cards_count = screen.textinput(f"Hello {player_name}", "\n\
Enter # of cards to play (8, 10, 12)")
            if cards_count is None:
                cards_count = 0
                player_name = None
                break
            elif cards_count.strip() == '' or not cards_count.isdigit():
                cards_count = 0
                continue
            cards_count = process_cards_and_start_game(cards_list, cards_count,
                                                       player_name)
    return True

def card_deck_clicked(card_path, title, card_deck_turtles, quit_btn):
    menu_screen_utils.load_card_deck_to_memory(card_path=card_path)
    title.hideturtle()
    title.clear()
    quit_btn.hideturtle()
    [card.turtle.hideturtle() for card in card_deck_turtles]
    process_is_success = request_details_and_start_game()
    
    if not process_is_success:
        load_card_selection_menu()
        
def load_card_decks(card_decks, card_deck_instances, screen, quit_button,
                    game_splash):
    for key, value in card_decks.items():
        screen.register_shape(value)
        card_deck_instances.append(Card(index=key+4, name=value, card_back
                                        =value))
        
        if key == list(card_decks.keys())[-1]:
            quit_button.showturtle()
        card_deck_instances[key].turtle.onclick(
            lambda x , y, card_path = value, title = game_splash, 
            card_deck_turtles = card_deck_instances, quit_btn = quit_button :\
                card_deck_clicked(
                card_path, title, card_deck_turtles, quit_btn))
         
def load_card_selection_menu():
    screen = turtle.Screen()
    card_decks = menu_screen_utils.load_menu_screen()
    if card_decks:
        game_splash = draw_utils.load_start_button(is_small=True)
        draw_utils.get_game_title(game_splash, is_small=True)
        game_splash.showturtle()
        card_deck_instances = []
        quit_button = draw_utils.load_quit_button()
        quit_button.hideturtle()
        start_btn = draw_utils.load_start_button()
        def handle_quit_button(x,y):
            game_splash.hideturtle()
            game_splash.clear()
            quit_button.hideturtle()
            [card.turtle.hideturtle() for card in card_deck_instances]
            time.sleep(0.5)
            draw_utils.get_game_title(start_btn)
            start_btn.showturtle()
        
        def handle_start_button(x,y):
            start_btn.hideturtle()
            start_btn.clear()
            load_card_selection_menu()
            
        start_btn.onclick(handle_start_button)    
        quit_button.onclick(handle_quit_button)  
        load_card_decks(card_decks, card_deck_instances, screen, quit_button,
                        game_splash)
       
def main():
    screen = turtle.Screen()
    draw_utils.draw_outlines()
    data_management_utils.register_assets(screen, ['quitbutton.gif', \
        'card_back.gif', 'winner.gif', 'quitmsg.gif', 'card_warning.gif', \
            'leaderboard_error.gif', 'file_error.gif'])
    start_btn = draw_utils.load_start_button()
    draw_utils.get_game_title(start_btn)
    draw_utils.load_quit_button()
    start_btn.showturtle()
    
    def handle_start_button(x,y):
        start_btn.hideturtle()
        start_btn.clear()
        load_card_selection_menu()

    start_btn.onclick(handle_start_button)
    screen.mainloop()

if __name__ == '__main__':
    main()