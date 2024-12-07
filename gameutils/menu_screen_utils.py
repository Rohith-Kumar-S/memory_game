"""
"""

import os
import random

def is_valid_asset_folder(path):
    try:
        files = os.listdir(path)
        if not files:
            return False
        for file in files:
            if not '.gif' in file:
                return False
        return True
    except FileNotFoundError:
        print(f'is_valid_asset_folder: {path} not found')
        return False
        

def reduce_to_relative_asset_path(card_path):
    game_directory = os.path.dirname((os.path.dirname(os.path.dirname(
        card_path))))
    relative_card_path = os.path.relpath(card_path, game_directory)
    return relative_card_path


def load_cards_from_card_deck(current_path):
    try:
        card_deck_path = os.path.dirname(current_path)
        cards_list = []
        for card in os.listdir(card_deck_path):
            cards_list.append(os.path.join(card_deck_path,card))
        return cards_list
    except FileNotFoundError:
        print(f'load_cards_from_card_deck: {current_path} not found')
        raise FileNotFoundError

def pick_one_card_from_each_asset(assets):
    menu_cards_list_dict = {}
    key = 0
    for asset in assets:
        file = random.choice(os.listdir(asset))
        menu_cards_list_dict[key] = os.path.join(asset,file)
        key += 1
    return menu_cards_list_dict

def load_card_deck_to_memory(card_path):
    try:
        cards_path_list = load_cards_from_card_deck(card_path)

        with open(os.path.join('config', 'memory.cfg'), mode='w') as f:
            for card_path in cards_path_list:
                card_path = reduce_to_relative_asset_path(card_path)
                f.write(f'{card_path}\n')
    except FileNotFoundError:
        print(f'load_card_deck_to_memory {card_path} not found')

def load_menu_screen():
    asset_path = os.path.join(os.getcwd(), 'assets')
    assets = os.listdir(os.path.join(os.getcwd(), 'assets'))
    assets = [os.path.join(asset_path, asset)  for asset in assets if not '.'
              in asset]
    valid_assets = [asset for asset in assets if is_valid_asset_folder(asset)]
    return pick_one_card_from_each_asset(valid_assets)
    
    