"""
CS 5001
Rohith Kumar Senthil Kumar
Project
"""

import turtle
import os
from card import Card
import time, random

def get_asset_path(path_list, screen):
    path_list.remove('')
    current_path = os.getcwd()
    for path in path_list:
        current_path = os.path.join(current_path, path.replace('\n',''))
    screen.register_shape(current_path)
    return current_path

def compare_cards(card_a, card_b):
    return card_a.name == card_b.name and card_a.index != card_b.index

def calculate_score(total_cards, total_clicks):
    return round(100*(total_cards/total_clicks))

def three_cards_clicked_at_once(card_handler_dict, active_card_index):
    return card_handler_dict['click_count']!=1 and card_handler_dict[
        'click_count'] %2 !=0 and active_card_index != None

def end_game(cards, card_handler_dict, players_dict, score_turtles, end_popup):
    players_dict[list(players_dict.keys())[-1]]["score"] = calculate_score(len(cards), card_handler_dict['click_count'])
    players_dict[list(players_dict.keys())[-1]]["clicks"] = card_handler_dict['click_count']
    player_key = list(players_dict.keys())[-1]
    players_dict = dict(sorted(players_dict.items(), key=lambda item: item[1]['clicks']))
    if len(players_dict) == 11:
        if list(players_dict.keys())[-1] == player_key:
            return
        else:
            key_to_be_deleted = list(players_dict.keys())[-1]
            del players_dict[key_to_be_deleted]
    load_score_board(players_dict, score_turtles)
    save_leaderboard_details(players_dict)
    end_popup.showturtle()
    
def process_card_actions(cards, active_card_index, current_card_index, 
                         card_handler_dict, action_turtles, column_value):
    if compare_cards(cards[active_card_index], cards[current_card_index]):
        time.sleep(1)
        cards[active_card_index].hide_card()
        cards[current_card_index].hide_card()
        card_handler_dict['right_choices'] += 1
    else:
        time.sleep(1)
        cards[active_card_index].reset_card()
        cards[current_card_index].reset_card()
    card_handler_dict['active_card_index'] = None
    load_player_action_details(card_handler_dict, action_turtles, column_value)    

def turtle_clicked(card_handler_dict, players_dict, current_card_index, 
                   score_turtles, action_turtles, column_value, end_popup):
    cards = card_handler_dict['cards']
    active_card_index = card_handler_dict['active_card_index']
    card_handler_dict['click_count'] += 1
    
    # restrict clicks to 2 per check
    if three_cards_clicked_at_once(card_handler_dict, active_card_index):
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
        
def update_action_turtles(action_turtles,card_handler_dict):
    for i, action in enumerate(action_turtles):
        action.clear()
        if i == 0:
            action.write('Gusses', move=False, align='left', font=('Arial', 12,
                                                                   'bold'))
            continue
        elif i == 1:
            action.write(str(card_handler_dict['click_count']//2), 
                         move=False, align='left', font=('Arial', 10, 'bold'))
            continue
        elif i == 2:
            action.write('Matches', move=False, align='left', 
                             font=('Arial', 12, 'bold'))
            continue
        elif i == 3:
            action.write(str(card_handler_dict['right_choices']), 
                         move=False, align='left', font=('Arial', 10, 'bold'))
        
def load_player_action_details(card_handler_dict, action_turtles, column_value):
    if action_turtles:
        update_action_turtles(action_turtles,card_handler_dict)         
    else:
        guesses_key = customize_turtle_text('Gusses', size=12, goto=(
            190, column_value-50))       
        action_turtles.append(guesses_key)
        guesses_value = customize_turtle_text(str(card_handler_dict[
            'click_count']//2), size=9, goto=(190, column_value-70))
        action_turtles.append(guesses_value)
        matches_key = customize_turtle_text('Matches', size=12, goto=(
            190, column_value-100))
        action_turtles.append(matches_key)
        matches_value = customize_turtle_text(str(card_handler_dict[
            'right_choices']), size=9, goto=(190, column_value-120))
        action_turtles.append(matches_value)
    return action_turtles

def load_score_board(players_dict, score_turtles):
    if score_turtles:
        reset_turtle(score_turtles)

    score_card_title = customize_turtle_text('Score card', size=12, goto=(190, 
             260))
    score_turtles.append(score_card_title)
    column_value = 240
    for i, (key, value) in enumerate(players_dict.items()):
        if value:
            column_value = 240 - (20 * i)
            text_to_display = f'{value['score']}    {key.split('#')[0]} : \
{value['clicks']}'
            text = customize_turtle_text(text_to_display, size=9, goto=(190, 
             column_value))
            score_turtles.append(text)
    return score_turtles, column_value


def customize_turtle_text(text, size, goto):
    t = turtle.Turtle()
    t.hideturtle()
    t.up()
    t.speed(10)
    t.penup()
    t.color('white')
    t.goto(goto)
    t.write(text, move=False, align='left', font=('Arial', size, 'bold'))
    return t

def load_cards(screen):
    cards_list = []
    try:
        with open('memory.cfg', mode='r') as f:
            for i, relative_path in enumerate(f):
                full_path = get_asset_path(
                    relative_path.split('\\'), screen)
                cards_list.append(full_path)
    except FileNotFoundError:
        error_message = load_pop_up('leaderboard_error.gif')
        error_message.showturtle()
        time.sleep(3)
        error_message.hideturtle()
    return cards_list

def initialize_card_handler():
    return {'active_card_index' : None,'click_count' : 0, 'right_choices' : 0, 
    'cards': [] }
    
def get_game_title(turtle_):
    turtle_.hideturtle()
    turtle_.goto(105,-20)
    turtle_.color('white')
    turtle_.write('MEMORY\n        GAME', move=False, align='right', font=(
        'Bauhaus 93', 48, 'bold'))
    turtle_.goto(-45,60)
    turtle_.color('red')

def reset_turtle(turtles):
    for turtle_ in turtles:
        turtle_.reset()
        turtle_.hideturtle()
        
def draw_and_play_cards(cards_list, card_handler_dict, players_dict, 
                        score_turtles, action_turtles, column_value, 
                        end_popup):
    for i, path in enumerate(cards_list):
        card_handler_dict['cards'].append(Card(index=i, name=path))
        card_handler_dict['cards'][i].turtle.onclick(
            lambda x , y, turtle_index = i : turtle_clicked(
                card_handler_dict, players_dict, turtle_index, score_turtles, 
                 action_turtles, column_value, end_popup))

def start_game(cards_list, players_dict, score_turtles, column_value, screen):
    card_handler_dict = initialize_card_handler()
    action_turtles = load_player_action_details(card_handler_dict, [], 
                                                column_value)
    end_popup = load_pop_up('winner.gif')
    draw_and_play_cards(cards_list, card_handler_dict, players_dict, 
                        score_turtles, action_turtles, column_value, end_popup)
    quit_button = load_quit_button()
    start_btn = load_start_button()
    quit_message = load_pop_up('quitmsg.gif')
    def handle_quit_button(x,y):
        nonlocal card_handler_dict
        end_popup.hideturtle()
        quit_message.showturtle()
        for card in card_handler_dict['cards']:
            card.turtle.hideturtle()
        reset_turtle(score_turtles)
        reset_turtle(action_turtles[-4:])
        quit_button.hideturtle()
        time.sleep(2)
        quit_message.hideturtle()
        get_game_title(start_btn)
        start_btn.showturtle()
        card_handler_dict = initialize_card_handler()
    
    def handle_start_button(x,y):
        start_btn.hideturtle()
        request_details_and_start_game(screen, start_btn)
        
    start_btn.onclick(handle_start_button)    
    quit_button.onclick(handle_quit_button)
        
def prepare_cards(cards_count, cards_list):
    cards_list = cards_list[:int(cards_count)//2]
    cards_list = cards_list+cards_list
    random.shuffle(cards_list)
    return cards_list

def get_leaderboard_details(players_dict):
    try:
        with open('leaderboard.txt', mode= 'r') as f:
            f.readline()
            for player_detail in f:
                player_name = player_detail.split()[0]
                player_score = player_detail.split()[1]
                player_clicks = player_detail.split()[2]
                players_dict[player_name] = {"score":player_score, 
                                                        "clicks" : int(
                                                            player_clicks)}
    except FileNotFoundError:
        error_message = load_pop_up('leaderboard_error.gif')
        error_message.showturtle()
        time.sleep(3)
        error_message.hideturtle()
        print('get_leaderboard_details: leaderboard.txt was not found!')
        
def save_leaderboard_details(players_dict):
    with open('leaderboard.txt', mode= 'w') as f:
        f.write('NAME\tSCORE\tCLICKS\n')
        for name, detail in players_dict.items():
            f.write(f'{name}\t{detail['score']}\t{detail['clicks']}\n')
            
def draw_cards_block():
    cards_border = turtle.Turtle()
    cards_border.speed(6)
    cards_border.penup()
    cards_border.hideturtle()
    cards_border.goto(-275,300)
    cards_border.pendown()
    cards_border.pensize(12)
    cards_border.pencolor((151,170,156))
    cards_border.begin_fill()
    cards_border.forward(450)
    cards_border.right(90)
    cards_border.forward(505)
    cards_border.right(90)
    cards_border.forward(450)
    cards_border.right(90)
    cards_border.forward(505)
    cards_border.end_fill()
    
def draw_score_board_block():
    score_border = turtle.Turtle()
    score_border.speed(6)
    score_border.penup()
    score_border.hideturtle()
    score_border.pencolor((151,170,156))
    score_border.fillcolor((151,170,156))
    score_border.goto(180,300)
    score_border.pensize(12)
    score_border.pendown()
    score_border.begin_fill()
    score_border.forward(150)
    score_border.right(90)
    score_border.forward(505)
    score_border.right(90)
    score_border.forward(150)
    score_border.right(90)
    score_border.forward(505)
    score_border.end_fill()
            
def draw_outlines():
    turtle.colormode(255)
    draw_cards_block()
    draw_score_board_block()
    
def is_card_count_odd(cards_count):
    return int(cards_count) != 1 and int(cards_count) % 2 != 0
    
def is_card_count_valid(cards_count, cards_list):
    return int(cards_count) % 2 == 0 and len(cards_list)*2 >= int(cards_count)
    
def process_game_parameters(player_name, cards_list, cards_count):
    players_dict = {}
    get_leaderboard_details(players_dict)
    players_dict[f'{player_name}#{len(players_dict.keys())}'] = {}
    score_turtles, column_value = load_score_board(players_dict, [])
    cards_list = prepare_cards(cards_count, cards_list)
    return players_dict, cards_list, score_turtles, column_value
    
def process_cards_and_start_game(cards_list, cards_count, player_name, 
                                 start_btn, screen):
    if is_card_count_odd(cards_count):
        warning_popup = load_pop_up('card_warning.gif')
        warning_popup.showturtle()
        time.sleep(3)
        warning_popup.hideturtle()
        cards_count = int(cards_count) - 1
    if is_card_count_valid(cards_count, cards_list):
        start_btn.clear()
        players_dict, cards_list, score_turtles, column_value = \
        process_game_parameters(player_name, cards_list, cards_count)
        start_game(cards_list, players_dict, score_turtles, column_value,
                   screen)
    else:
        cards_count = 0
    return cards_count
    
    
def request_details_and_start_game(screen, start_btn):
    player_name = None
    cards_count = 0
    cards_list = load_cards(screen)
    
    while player_name == None:
        player_name = screen.textinput("Welcome to the Memory Game!", \
"Enter your name")
        if player_name is None:
            screen.bye()
            break
        elif player_name.strip() == '':
            continue
        
        while cards_count == 0:
            cards_count = screen.textinput(f"Hello {player_name}", "Please \
enter the number of cards to play (8, 10, 12)")
            if cards_count is None:
                cards_count = 0
                player_name = None
                break
            elif cards_count.strip() == '' or not cards_count.isdigit():
                cards_count = 0
                continue
            cards_count = process_cards_and_start_game(cards_list, cards_count,
                                                       player_name, start_btn, 
                                                        screen)
                        
def load_quit_button():
    return load_custom_turtle('quitbutton.gif',goto=(250,-135), 
                              showturtle=True)

def load_pop_up(asset_name):
    return load_custom_turtle(asset_name, goto=(-55,60), showturtle=False)
    
def load_custom_turtle(asset_name, goto, showturtle=False):
    turtle_ = turtle.Turtle()
    turtle_.hideturtle()
    turtle_.penup()
    turtle_.up()
    turtle_.goto(goto)
    turtle_.pendown()
    if showturtle:
        turtle_.showturtle()
    turtle_.shape(os.path.join(os.path.join(os.getcwd(), 'assets'),
                                  asset_name))
    return turtle_
                
def load_start_button():
    start_btn = turtle.Turtle("triangle")
    start_btn.hideturtle()
    start_btn.penup()
    start_btn.goto(-45,60)
    start_btn.turtlesize(4)
    return start_btn
    
def register_assets(screen, assets):
    for asset in assets:
        screen.register_shape(os.path.join(os.path.join(os.getcwd(), 'assets'),
                                       asset))
    
def main():
    screen = turtle.Screen()
    draw_outlines()
    register_assets(screen, ['quitbutton.gif', 'card_back.gif', 'winner.gif', \
        'quitmsg.gif', 'card_warning.gif', 'leaderboard_error.gif', \
            'file_error.gif'])
    start_btn = load_start_button()
    get_game_title(start_btn)
    quit_button = load_quit_button()
    start_btn.showturtle()
    
    def handle_start_button(x,y):
        start_btn.hideturtle()
        request_details_and_start_game(screen,start_btn)
    
    def handle_quit_button(x,y):
        screen.bye()
    
    start_btn.onclick(handle_start_button)
    quit_button.onclick(handle_quit_button)
    screen.mainloop()
    
   

if __name__ == '__main__':
    main()