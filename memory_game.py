"""
CS 5001
Rohith Kumar Senthil Kumar
Fall 2024

Memory Game - Project
"""

import turtle
from model.card import Card
import time
from gameutils import menu_screen_utils
from gameutils import card_utils
from gameutils import draw_utils
from gameutils import data_management_utils

def end_game(cards, card_handler_dict, players_dict, score_turtles, end_popup):
    """end_game: Triggered after all the cards are guessed, it updates the 
    scoreboard with the player's score. The player is ranked based on their 
    score compared to previous players. The scores are saved to a file, and a 
    winning popup is displayed.

    Args:
        cards (_type_): represents the list of Card classes 
        card_handler_dict (_type_): main gameplay details dictionary
        players_dict (_type_): player details dicitonary
        score_turtles (_type_): turtle list which display the score board
        end_popup (_type_): a turtle instance which represents the wining popup
    """
    try:
        players_dict[list(players_dict.keys())[-1]]["score"] = \
            card_utils.calculate_score(len(cards), card_handler_dict['click_count'
                                                                    ])
        players_dict[list(players_dict.keys())[-1]]["clicks"] = \
            card_handler_dict['click_count']
        player_key = list(players_dict.keys())[-1]
        
        # sort based on score
        players_dict = data_management_utils.sort_based_on_score(players_dict)
        
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
    except Exception as e:
        print('error: something went wrong in process_card_actions():', str(e))  
    
def process_card_actions(cards, active_card_index, current_card_index, 
                         card_handler_dict, action_turtles, column_value):
    """process_card_actions: Takes in the details of the previously clicked 
    card and the currently clicked card, compares them, and updates the 
    card_handler_dict if a correct match is made. Invokes the function to 
    update the guess count and match count.

    Args:
        cards (list): represents the list of Card classes
        active_card_index (_type_): index of the previous clicked card
        current_card_index (_type_): index of the current clicked card
        card_handler_dict (_type_): main gameplay details dictionary
        action_turtles (_type_): turtle list which display the guesses and 
                                 matches
        column_value (_type_): used for the position adjustment of the score
                               details
    """
    try:
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
    except Exception as e:
        print('error: something went wrong in process_card_actions()', str(e))  

def card_clicked(card_handler_dict, players_dict, current_card_index, 
                   score_turtles, action_turtles, column_value, end_popup):
    """card_clicked: Triggered when a card is clicked. Stores the index of the 
    clicked card, and if two cards have been clicked, it proceeds to compare 
    them and updates the card_handler_dict. If all cards are clicked and 
    correctly matched, it proceeds to end the game.

    Args:
        card_handler_dict (_type_): main gameplay details dictionary
        players_dict (_type_): player details dicitonary
        current_card_index (_type_): index of the current clicked card
        score_turtles (_type_): turtle list which display the score board
        action_turtles (_type_): turtle list which display the guesses and 
                                 matches
        column_value (_type_): used for the position adjustment of the score
                               details
        end_popup (_type_): a turtle instance which represents the wining popup
    """
    try:
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
    except Exception as e:
        print('error: something went wrong in card_clicked()', str(e))
        
def draw_and_play_cards(cards_list, card_handler_dict, players_dict, 
                        score_turtles, action_turtles, column_value, 
                        end_popup):
    """draw_and_play_cards: creates instances of the Card class based on the
    cards_list. On click of a card calls the card_clicked function.

    Args:
        cards_list (_type_): list of card paths from the chosen card deck
        card_handler_dict (_type_): main gameplay details dictionary
        players_dict (_type_): player details dicitonary
        score_turtles (_type_): turtle list which display the score board
        action_turtles (_type_): turtle list which display the guesses and 
                                 matches
        column_value (_type_): used for the position adjustment of the score
                               details
        end_popup (_type_): a turtle instance which represents the wining popup
    """
    
    try:
        for i, path in enumerate(cards_list):
            card_handler_dict['cards'].append(Card(index=i, name=path))
            card_handler_dict['cards'][i].turtle.onclick(
                lambda x , y, turtle_index = i : card_clicked(
                    card_handler_dict, players_dict, turtle_index, 
                    score_turtles, action_turtles, column_value, end_popup))
    except Exception as e:
        print('error: something went wrong in draw_and_play_cards()', str(e))

def handle_in_game_quit_button(end_popup, quit_message, quit_button, 
                               score_turtles, action_turtles, start_btn, 
                               card_handler_dict):
    """handle_in_game_quit_button: Handles the click event for the quit button
    which is generated on the start of a new game. Here new game referes to the
    gameplay after the user chooses a card deck to play with.

    Args:
        end_popup (_type_): a turtle instance which represents the wining popup
        quit_message (_type_): a turtle instance which represents the quit 
                               game popup
        quit_button (_type_): a turtle instance which represents the quit 
                               button
        score_turtles (_type_): turtle list which display the score board
        action_turtles (_type_): turtle list which display the guesses and 
                                 matches
        start_btn (_type_): a turtle instance which represents the start
                               button
        card_handler_dict (_type_): main gameplay details dictionary
    """
    try:
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
    except Exception as e:
        print('error: something went wrong in handle_in_game_quit_button()', 
              str(e))

def start_game(cards_list, players_dict, score_turtles, column_value):
    """start_game: starts the game after a card deck was chosen and after the 
    user enters their details. Initializes the game elements and the 
    card_handler_dict which records the details of the gameplay

    Args:
        cards_list (_type_): list of card paths from the chosen card deck
        players_dict (_type_): player details dicitonary
        score_turtles (_type_): turtle list which display the score board
        column_value (_type_): used for the position adjustment of the score
                               details
    """
    
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
            """handle_quit_button: handles on click event of quit button
            """
            
            nonlocal card_handler_dict
            handle_in_game_quit_button(end_popup, quit_message, quit_button, 
                               score_turtles, action_turtles, start_btn, 
                               card_handler_dict)
        
        def handle_start_button(x,y):
            """handle_start_button: handles on click event of start button
            """
            
            start_btn.hideturtle()
            start_btn.clear()
            load_card_selection_menu()
            
        start_btn.onclick(handle_start_button)    
        quit_button.onclick(handle_quit_button)
    except Exception as e:
        print('error: something went wrong in start_game()', str(e))
    
def process_cards_and_start_game(cards_list, cards_count, player_name):
    """process_cards_and_start_game: Performs checks on the card count entered 
    by the user and starts the game based on the result. Initializes various
    ingame parameters including player details and score details.

    Args:
        cards_list (_type_): list of card paths from the chosen card deck
        cards_count (_type_): user entered count of the cards to play with
        player_name (_type_): name of the player or user

    Returns:
        int : returns card count as 0 incase of invalid input, which prompts
        the user to enter the count again
    """
    
    try:
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
    except Exception as e:
        print('error: something went wrong in process_cards_and_start_game()'
              , str(e))
    
def request_details_and_start_game():
    """request_details_and_start_game: Requests the player's details and starts
    the game. Continues prompting the user for input in case of invalid entries
    """
    
    try:
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
    except Exception as e:
        print('error: something went wrong in request_details_and_start_game()'
              , str(e))

def card_deck_clicked(card_path, title, card_deck_turtles, quit_btn, info_txt):
    """card_deck_clicked: triggered when a card deck is clicked.

    Args:
        card_path (_type_): path of the card deck clicked
        title (_type_): turtle instance representing game splash art 
        card_deck_turtles (_type_): list of tuurtles reprenting the card decks
                                    available in the assets folder
        quit_btn (_type_): a turtle instance which represents the quit 
                               button
    """
    
    try:
        menu_screen_utils.load_card_deck_to_memory(card_path=card_path)
        title.hideturtle()
        title.clear()
        info_txt.hideturtle()
        info_txt.clear()
        quit_btn.hideturtle()
        [card.turtle.hideturtle() for card in card_deck_turtles]
        process_is_success = request_details_and_start_game()
        
        if not process_is_success:
            load_card_selection_menu()
    except Exception as e:
        print('error: something went wrong in card_deck_clicked()', str(e))
        
def load_card_decks(card_decks, card_deck_instances, screen, quit_button,
                    info_text, game_splash):
    """load_card_decks: loads the card decks in the card deck selection menu 
    screen. Onclick of a card deck, card_deck_clicked function is called.

    Args:
        card_decks (_type_): _description_
        card_deck_instances (_type_): _description_
        screen (_type_): _description_
        quit_button (_type_): _description_
        game_splash (_type_): _description_
    """
    
    try:
        for key, value in card_decks.items():
            screen.register_shape(value)
            card_deck_instances.append(Card(index=key+4, name=value, card_back
                                            =value))
            
            if key == list(card_decks.keys())[-1]:
                quit_button.showturtle()
            card_deck_instances[key].turtle.onclick(
                lambda x , y, card_path = value, title = game_splash, 
                card_deck_turtles = card_deck_instances, quit_btn = \
                    quit_button, info_txt = info_text : card_deck_clicked(
                    card_path, title, card_deck_turtles, quit_btn, info_txt))
    except Exception as e:
        print('error: something went wrong in load_card_decks()', str(e))
         
def load_card_selection_menu():
    """load_card_selection_menu: loads the card deck selection menu 
    screen which displays the card decks for the user or the player to choose
    """
    
    try:
        screen = turtle.Screen()
        card_decks = menu_screen_utils.load_menu_screen_data()
        if card_decks:
            game_splash = draw_utils.load_start_button(is_small=True)
            draw_utils.get_game_title(game_splash, is_small=True)
            game_splash.showturtle()
            info_text = draw_utils.customize_turtle_text(
                'Pick a card deck', 10, (-250, 125), font = 'Century Gothic')
            card_deck_instances = []
            quit_button = draw_utils.load_quit_button()
            quit_button.hideturtle()
            start_btn = draw_utils.load_start_button()
            def handle_quit_button(x,y):
                """handle_quit_button: handles on click event of auick button
                """
                
                game_splash.hideturtle()
                game_splash.clear()
                info_text.hideturtle()
                info_text.clear()
                quit_button.hideturtle()
                [card.turtle.hideturtle() for card in card_deck_instances]
                time.sleep(0.5)
                draw_utils.get_game_title(start_btn)
                start_btn.showturtle()
            
            def handle_start_button(x,y):
                """handle_start_button: handles on click event of start button
                """
                
                start_btn.hideturtle()
                start_btn.clear()
                load_card_selection_menu()
                
            start_btn.onclick(handle_start_button)    
            quit_button.onclick(handle_quit_button)  
            load_card_decks(card_decks, card_deck_instances, screen, 
                            quit_button, info_text, game_splash)
    except Exception as e:
        print('error: something went wrong in load_card_selection_menu()', 
              str(e))
       
def main():
    """Initiates the gameplay, generates the base game elements. loads the
    card deck selection menu screen on click of the start_btn
    """
    
    try:
        screen = turtle.Screen()
        draw_utils.draw_outlines()
        draw_utils.load_developer_signature()
        data_management_utils.register_assets(screen, ['quitbutton.gif', \
            'card_back.gif', 'winner.gif', 'quitmsg.gif', 'card_warning.gif', \
                'leaderboard_error.gif', 'file_error.gif'])
        start_btn = draw_utils.load_start_button()
        draw_utils.get_game_title(start_btn)
        draw_utils.load_quit_button()
        start_btn.showturtle()
        
        def handle_start_button(x,y):
            """handle_start_button: handles on click event of start button
            """
                
            start_btn.hideturtle()
            start_btn.clear()
            load_card_selection_menu()

        start_btn.onclick(handle_start_button)
        screen.mainloop()
    except Exception as e:
        print('error: something went wrong in main()', str(e))

if __name__ == '__main__':
    main()