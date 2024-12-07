from . import card_utils
from . import draw_utils
import time
import os

def get_leaderboard_details(players_dict):
    try:
        with open(os.path.join('config', 'leaderboard.txt'), mode= 'r') as f:
            f.readline()
            for player_detail in f:
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
    with open(os.path.join('config', 'leaderboard.txt'), mode= 'w') as f:
        f.write('NAME\tSCORE\tCLICKS\n')
        for name, detail in players_dict.items():
            f.write(f'{name}\t{detail['score']}\t{detail['clicks']}\n')
    
def process_game_parameters(player_name, cards_list, cards_count):
    players_dict = {}
    get_leaderboard_details(players_dict)
    players_dict[f'{player_name}#{len(players_dict.keys())}'] = {}
    score_turtles, column_value = draw_utils.load_score_board(players_dict, [])
    cards_list = card_utils.prepare_cards(cards_count, cards_list)
    return players_dict, cards_list, score_turtles, column_value

def load_cards(screen):
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
    for asset in assets:
        if not is_full_path:
            screen.register_shape(os.path.join(os.path.join(os.getcwd(), 
                                                            'assets'), asset))
        else:
            screen.register_shape(os.path.join(os.path.join(os.getcwd(), 
                                                            'assets'), asset))