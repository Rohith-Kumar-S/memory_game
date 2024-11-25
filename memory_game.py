"""_summary_
"""

import turtle
import os
from card import Card
import time, random
import threading



def get_asset_path(path_list, screen):
    path_list.remove('')
    current_path = os.getcwd()
    for path in path_list:
        current_path = os.path.join(current_path, path.replace('\n',''))
    
    screen.register_shape(os.path.join(os.path.join(os.getcwd(), 'assets'),
                                       'card_back.gif'))
    screen.register_shape(os.path.join(os.path.join(os.getcwd(), 'assets'),
                                       'winner.gif'))
    screen.register_shape(os.path.join(os.path.join(os.getcwd(), 'assets'),
                                       'quitmsg.gif'))
    screen.register_shape(current_path)
    return current_path

def compare_cards(card_a, card_b):
    print(card_a.index, card_b.index)
    return card_a.name == card_b.name and card_a.index != card_b.index

def calculate_score(total_cards, total_clicks):
    return round(100*(total_cards/total_clicks))


def turtle_clicked(card_handler_dict, players_dict, current_card_index, score_turtles, action_turtles, column_value, end_popup):
    cards = card_handler_dict['cards']
    active_card_index = card_handler_dict['active_card_index']
    card_handler_dict['click_count'] += 1
    
    # restrict clicks to 2 per check
    if card_handler_dict['click_count']!=1 and\
         card_handler_dict['click_count'] %2 !=0 and active_card_index != None:
        card_handler_dict['click_count'] -= 1
        return
        
    cards[current_card_index].flip_card()
    if active_card_index != None:
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
    else:
        card_handler_dict['active_card_index'] = current_card_index
    if card_handler_dict['right_choices'] == len(cards)//2:
        players_dict[list(players_dict.keys())[-1]]["score"] = calculate_score(len(cards), card_handler_dict['click_count'])
        players_dict[list(players_dict.keys())[-1]]["clicks"] = card_handler_dict['click_count']
        print(f'game over!, total clicks: {card_handler_dict['click_count']}, your score: {calculate_score(len(cards), card_handler_dict['click_count'])}')
        player_key = list(players_dict.keys())[-1]
        players_dict = dict(sorted(players_dict.items(), key=lambda item: item[1]['clicks']))
        if len(players_dict) == 11:
           if list(players_dict.keys())[-1] == player_key:
               return
           else:
               key_to_be_deleted = list(players_dict.keys())[-1]
               del players_dict[key_to_be_deleted]
        print(players_dict)
        load_score_board(players_dict, score_turtles)
        save_leaderboard_details(players_dict)
        end_popup.showturtle()
        
def load_player_action_details(card_handler_dict, action_turtles, column_value):
    print(column_value)
    if action_turtles:
        for i, action in enumerate(action_turtles):
            action.clear()
            if i == 0:
                action.write('Gusses', move=False, align='left', font=('Arial', 12, 'bold'))
                continue
            elif i == 1:
                action.write(str(card_handler_dict['click_count']//2), move=False, align='left', font=('Arial', 10, 'bold'))
                continue
            elif i == 2:
                action.write('Matches', move=False, align='left', font=('Arial', 12, 'bold'))
                continue
            elif i == 3:
                action.write(str(card_handler_dict['right_choices']), move=False, align='left', font=('Arial', 10, 'bold'))
                
    else:       
        guesses_key = turtle.Turtle()
        guesses_key.hideturtle()
        guesses_key.up()
        guesses_key.speed(10)
        guesses_key.penup()
        guesses_key.goto(190, column_value-50)
        guesses_key.color('white')
        guesses_key.write('Gusses', move=False, align='left', font=('Arial', 12, 'bold'))
        action_turtles.append(guesses_key)
        guesses_value = turtle.Turtle()
        guesses_value.hideturtle()
        guesses_value.up()
        guesses_value.penup()
        guesses_value.goto(190, column_value-70)
        guesses_value.color('white')
        # print(card_handler_dict)
        guesses_value.write(str(card_handler_dict['click_count']//2), move=False, align='left', font=('Arial', 9, 'bold'))
        action_turtles.append(guesses_value)
        matches_key = turtle.Turtle()
        matches_key.hideturtle()
        matches_key.speed(10)
        matches_key.up()
        matches_key.penup()
        matches_key.goto(190, column_value-100)
        matches_key.color('white')
        matches_key.write('Matches', move=False, align='left', font=('Arial', 12, 'bold'))
        action_turtles.append(matches_key)
        matches_value = turtle.Turtle()
        matches_value.speed(10)
        matches_value.hideturtle()
        matches_value.up()
        matches_value.penup()
        matches_value.goto(190, column_value-120)
        matches_value.color('white')
        matches_value.write(str(card_handler_dict['right_choices']), move=False, align='left', font=('Arial', 9, 'bold'))
        action_turtles.append(matches_value)
    return action_turtles

def load_score_board(players_dict, score_turtles):
    if score_turtles:
        for score in score_turtles:
            score.reset()
            score.hideturtle()
    
    row1 = turtle.Turtle()
    row1.hideturtle()
    row1.up()
    row1.penup()
    row1.goto(190, 260)
    row1.color('white')
    row1.write('Score card', move=False, align='left', font=('Arial', 12, 'bold'))
    score_turtles.append(row1)
    column_value = 240
    for i, (key, value) in enumerate(players_dict.items()):
        if value:
            text = turtle.Turtle()
            text.hideturtle()
            text.up()
            text.speed(8)
            text.penup()
            text.color('white')
            column_value = 240 - (20 * i)
            text.goto(190, column_value)
            text.write(f'{value['score']}    {key.split('#')[0]} : {value['clicks']}', move=False, align='left', font=('Arial', 9, 'bold'))
            score_turtles.append(text)
    return score_turtles, column_value

def load_cards(screen):
    cards_list = []
    with open('memory.cfg', mode='r') as f:
        for i, relative_path in enumerate(f):
            full_path = get_asset_path(
                relative_path.split('\\'), screen)
            cards_list.append(full_path)
    return cards_list

def initialize_card_handler():
    return {'active_card_index' : None,'click_count' : 0, 'right_choices' : 0, 'cards': [] }

def start_game(cards_list, players_dict, score_turtles, column_value, screen):
    card_handler_dict = initialize_card_handler()
    action_turtles = load_player_action_details(card_handler_dict, [], column_value)
    end_popup = end_game()
    for i, path in enumerate(cards_list):
        card_handler_dict['cards'].append(Card(index=i, name=path))
        card_handler_dict['cards'][i].turtle.onclick(
            lambda x , y, turtle_index = i : turtle_clicked(
                card_handler_dict, players_dict, turtle_index, score_turtles, 
                 action_turtles, column_value, end_popup))
    quit_button = load_quit_button()
    menu = start_button()
    quit_message = load_quitmsg()
    def handle_quit_button(x,y):
        print('quit_btn clicked')
        nonlocal card_handler_dict
        nonlocal menu
        end_popup.hideturtle()
        quit_message.showturtle()
        for card in card_handler_dict['cards']:
            card.turtle.hideturtle()
        for score in score_turtles:
            score.reset()
            score.hideturtle()
        for action in action_turtles[-4:]:
            action.reset()
            action.hideturtle()
        quit_button.hideturtle()
        time.sleep(2)
        quit_message.hideturtle()
        menu.showturtle()
        card_handler_dict = initialize_card_handler()
    
    def handle_start_button(x,y):
        menu.hideturtle()
        start(screen)
        
    menu.onclick(handle_start_button)    
    quit_button.onclick(handle_quit_button)
    
    
        
def prepare_cards(cards_count, cards_list):
    cards_list = cards_list[:int(cards_count)//2]
    cards_list = cards_list+cards_list
    random.shuffle(cards_list)
    return cards_list

def end_game():
    print('end')
    t = turtle.Turtle()
    t.up()
    t.hideturtle()
    t.penup()
    t.speed(10)
    t.goto(-55,60)
    t.shape(os.path.join(os.path.join(os.getcwd(), 'assets'),
                                       'winner.gif'))
    return t

def get_leaderboard_details(players_dict):
    try:
        with open('leaderboard.txt', mode= 'r') as f:
            f.readline()
            for player_detail in f:
                player_name = player_detail.split()[0]
                player_score = player_detail.split()[1]
                player_clicks = player_detail.split()[2]
                players_dict[player_name] = {"score":player_score, 
                                                        "clicks" : int(player_clicks)}
                print(players_dict)
    except FileNotFoundError:
        print('get_leaderboard_details: leaderboard.txt was not found!')
        
def save_leaderboard_details(players_dict):
    with open('leaderboard.txt', mode= 'w') as f:
        f.write('NAME\tSCORE\tCLICKS\n')
        for name, detail in players_dict.items():
            f.write(f'{name}\t{detail['score']}\t{detail['clicks']}\n')
            
def draw_outlines():
    turtle.colormode(255)
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
    
def start(screen):
    player_name = None
    cards_count = 0
    cards_list = load_cards(screen)
    while player_name == None:
        pop_up_screen = turtle.Screen()
        player_name = pop_up_screen.textinput("Welcome to the Memory Game!", "Enter your name")
        # player_name = 'test'
        if player_name is None:
            screen.bye()
            break
        elif player_name.strip() == '':
            continue
        
        while cards_count == 0:
            cards_count = pop_up_screen.textinput(f"Hello {player_name}", "Please enter the number of cards to play (8, 10, 12)")
            # cards_count = '12'
            if cards_count is None:
                print('breaking')
                cards_count = 0
                player_name = None
                break
            elif cards_count.strip() == '' or not cards_count.isdigit():
                cards_count = 0
                continue
            
            if int(cards_count) !=1 and int(cards_count) % 2 != 0:
                cards_count = int(cards_count) - 1
                
            if int(cards_count) % 2 == 0 and len(cards_list)*2 >= int(cards_count):
                players_dict = {}
                get_leaderboard_details(players_dict)
                players_dict[f'{player_name}#{len(players_dict.keys())}'] = {}
                print(players_dict)
                score_turtles, column_value = load_score_board(players_dict, [])
                cards_list = prepare_cards(cards_count, cards_list)
                start_game(cards_list, players_dict, score_turtles, column_value,screen)
            else:
                cards_count = 0
                
def load_quit_button():
    quit_button = turtle.Turtle()
    quit_button.hideturtle()
    quit_button.penup()
    quit_button.up()
    quit_button.goto(250,-135)
    quit_button.pendown()
    quit_button.showturtle()
    quit_button.shape(os.path.join(os.path.join(os.getcwd(), 'assets'),
                                  'quitbutton.gif'))
    return quit_button
    
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
    
def load_quitmsg():
    return load_custom_turtle('quitmsg.gif',goto=(-55,60), showturtle=False)
                
def start_button():
    menu = turtle.Turtle("triangle")
    menu.hideturtle()
    menu.penup()
    menu.color('white')
    menu.turtlesize(6)
    menu.goto(-45,60)
    # menu.write('Play', move=False, align='center', font=('Arial', 24, 'bold'))
    return menu

def main():
    screen = turtle.Screen()
    def my_click_handler(x, y):
        print(f"You clicked at (x:{x}, y:{y})")

    # screen.onclick(my_click_handler)
    draw_outlines()
    screen.register_shape(os.path.join(os.path.join(os.getcwd(), 'assets'),
                                       'quitbutton.gif'))
    
    
    
    menu = start_button()
    quit_button = load_quit_button()
    menu.showturtle()
    def handle_start_button(x,y):
        nonlocal screen
        nonlocal menu
        menu.hideturtle()
        start(screen)
    
    def handle_quit_button(x,y):
        nonlocal screen
        nonlocal menu
        screen.bye()
    
    
    menu.onclick(handle_start_button)
    quit_button.onclick(handle_quit_button)
    
    
    
   

    
    
    

            
            
            
    
    
    
    
    screen.mainloop()
    
   

if __name__ == '__main__':
    main()