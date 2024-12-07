import turtle
import os
from . import card_utils

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
                
def load_start_button(is_small=False):
    start_btn = turtle.Turtle("triangle")
    start_btn.hideturtle()
    start_btn.penup()
    goto = (-45,60) if not is_small else (-195,240)
    start_btn.goto(goto)
    start_btn.turtlesize(4)
    return start_btn

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
        
def load_player_action_details(card_handler_dict, action_turtles, 
                               column_value):
    if action_turtles:
        update_action_turtles(action_turtles,card_handler_dict)         
    else:
        guesses_key = customize_turtle_text(
            'Gusses', size=12, goto=(190, column_value-50))       
        action_turtles.append(guesses_key)
        guesses_value = customize_turtle_text(str(card_handler_dict[
            'click_count']//2), size=9, goto=(190, column_value-70))
        action_turtles.append(guesses_value)
        matches_key = customize_turtle_text(
            'Matches', size=12, goto=(190, column_value-100))
        action_turtles.append(matches_key)
        matches_value = customize_turtle_text(str(card_handler_dict[
            'right_choices']), size=9, goto=(190, column_value-120))
        action_turtles.append(matches_value)
    return action_turtles

def load_score_board(players_dict, score_turtles):
    if score_turtles:
        card_utils.reset_turtle(score_turtles)

    score_card_title = customize_turtle_text('Score card', size=12, 
                                                        goto=(190, 260))
    score_turtles.append(score_card_title)
    column_value = 240
    for i, (key, value) in enumerate(players_dict.items()):
        if value:
            column_value = 240 - (20 * i)
            text_to_display = f' {value['score']}    {key.split('#')[0]}    \
{value['clicks']}'
            text = customize_turtle_text(text_to_display, size=9, 
            goto=(190, column_value))
            score_turtles.append(text)
    return score_turtles, column_value
    
def customize_turtle_text(text, size, goto):
    print(goto, type(goto))
    t = turtle.Turtle()
    t.hideturtle()
    t.up()
    t.speed(10)
    t.penup()
    t.color('white')
    t.goto(goto)
    t.write(text, move=False, align='left', font=('Arial', size, 'bold'))
    return t
    
def get_game_title(turtle_, is_small=False):
    turtle_.hideturtle()
    goto = (105,-20) if not is_small else (-85,190)
    turtle_.goto(goto)
    turtle_.color('white')
    turtle_.write('MEMORY\n        GAME', move=True, align='right', font=(
        'Bauhaus 93', 48 if not is_small else 22, 'bold'))
    goto = (-45,60) if not is_small else (-156,225)
    turtle_.goto(goto)
    if is_small:
        turtle_.turtlesize(1.7)
    turtle_.color('red')