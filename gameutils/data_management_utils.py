"""
CS 5001
Rohith Kumar Senthil Kumar
Fall 2024

funtions to handle the game data
"""

from . import card_utils
from . import draw_utils
import time
import os

def get_leaderboard_details(players_dict):
    """get_leaderboard_details: retrives the leaderboard details from txt file
    and updates it to the players_dict

    Args:
        players_dict (_type_): player details dicitonary
    """
    
    try:
        with open(os.path.join('config', 'leaderboard.txt'), mode= 'r') as f:
            f.readline()
            for player_detail in f:
                player_detail = player_detail.strip()
                player_name = player_detail.split()[0]
                player_score = player_detail.split()[1]
                player_clicks = player_detail.split()[2]
                players_dict[player_name] = {"score":player_score, 
                                                        "clicks" : int(
                                                            player_clicks)}
    except FileNotFoundError:
        error_message = draw_utils.load_pop_up('leaderboard_error.gif')
        error_message.showturtle()
        time.sleep(3)
        error_message.hideturtle()
        print('get_leaderboard_details: leaderboard.txt was not found!')
        
def save_leaderboard_details(players_dict):
    """save_leaderboard_details: persists the updates players scores to a file

    Args:
        players_dict (_type_): player details dicitonary
    """
    
    with open(os.path.join('config', 'leaderboard.txt'), mode= 'w') as f:
        f.write('NAME\tSCORE\tCLICKS\n')
        for name, detail in players_dict.items():
            f.write(f'{name}\t{detail['score']}\t{detail['clicks']}\n')
    
def process_game_parameters(player_name, cards_list, cards_count):
    """process_game_parameters: populates data for score, prepares the cards 
    based on count and updates the current player details to the players_dict

    Args:
        player_name (_type_): name of the player
        cards_list (_type_): list of card paths from the card deck 
        cards_count (_type_): user inputS
    """
    
    players_dict = {}
    get_leaderboard_details(players_dict)
    players_dict[f'{player_name}#{len(players_dict.keys())}'] = {}
    score_turtles, column_value = draw_utils.load_score_board(players_dict, [])
    cards_list = card_utils.prepare_cards(cards_count, cards_list)
    return players_dict, cards_list, score_turtles, column_value

def load_cards(screen):
    """load_cards: loads the cards path from the meomory.txt file and appends
    it ti the cards_list

    Args:
        screen (_type_): turtle screen

    Returns:
        cards_list: list of card paths from the card deck 
    """
    
    cards_list = []
    try:
        with open(os.path.join('config', 'memory.cfg'), mode='r') as f:
            for i, relative_path in enumerate(f):
                full_path = os.path.join(os.getcwd(),relative_path).strip()
                screen.register_shape(full_path)
                cards_list.append(full_path)
    except FileNotFoundError:
        error_message = draw_utils.load_pop_up('file_error.gif')
        error_message.showturtle()
        time.sleep(3)
        error_message.hideturtle()
        
    return cards_list

def register_assets(screen, assets, is_full_path = False):
    """register_assets: registers the assets passed to the turtle screen

    Args:
        screen (_type_): turtle screen
        assets (_type_): asset file name
        is_full_path (bool, optional): if True assets is a full path. Defaults 
                                       to False.
    """
    
    for asset in assets:
        if not is_full_path:
            screen.register_shape(os.path.join(os.path.join(os.getcwd(), 
                                                            'assets'), asset))
        else:
            screen.register_shape(os.path.join(os.path.join(os.getcwd(), 
                                                            'assets'), asset))