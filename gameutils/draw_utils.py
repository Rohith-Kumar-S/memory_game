"""
CS 5001
Rohith Kumar Senthil Kumar
Fall 2024

funtions that builds the user interface
"""

import turtle
import os
from . import card_utils
import time

def draw_cards_block():
    """draw_cards_block: draws the game design
    """
    
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
    """draw_cards_block: draws the score_board_block
    """
    
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
    
def load_developer_signature():
    """load_developer_signature: loads a text with developer's name
    """
    
    time.sleep(1)
    info_text_1 = customize_turtle_text(
        'Developed by', 12, (-100, 65), font = 'Century Gothic')
    info_text_2 = customize_turtle_text(
        'Rohith Kumar S', 15, (-115, 25), font = 'Century Gothic')
    time.sleep(3)
    info_text_1.clear()
    info_text_2.clear()
            
def draw_outlines():
    """draw_outlines: calls the draw game design functions
    """
    
    turtle.colormode(255)
    draw_cards_block()
    draw_score_board_block()
    
def load_quit_button():
    """load_quit_button: load quit button

    Returns:
        turtle: a turtle instance representing a quit button
    """
    
    return load_custom_turtle('quitbutton.gif',goto=(250,-135), 
                              showturtle=True)

def load_pop_up(asset_name):
    """load_pop_up: calls a custom popup, passes the asset_name to it

    Args:
        asset_name (_type_): path of the file

    Returns:
       turtle: a turtle instance representing a quit button
    """
    
    return load_custom_turtle(asset_name, goto=(-55,60), showturtle=False)
    
def load_custom_turtle(asset_name, goto, showturtle=False):
    """load_custom_turtle: creates a turtle instance which can be used as a
    popup

    Args:
        asset_name (_type_): path of the file
        goto (_type_): position in the screen to goto
        showturtle (bool, optional): True to show the turtle Defaults to False.

    Returns:
        turtle: a turtle instance representing a quit button
    """
    
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
    """load_start_button: loads the title game splash art

    Args:
        is_small (bool, optional): If true will be used for card deck screen
        . Defaults to False.

    Returns:
        turtle: a turtle instance representing a quit button
    """
    
    start_btn = turtle.Turtle("triangle")
    start_btn.hideturtle()
    start_btn.penup()
    goto = (-45,60) if not is_small else (-195,240)
    start_btn.goto(goto)
    start_btn.turtlesize(4)
    return start_btn

def update_action_turtles(action_turtles,card_handler_dict):
    """update_action_turtles: Updates the text for guesses and matches after 
    each card action initiated by the user

    Args:
        action_turtles (_type_): list of turtle instances representing guesses 
                                 and matches
        card_handler_dict (_type_): main gameplay details dictionary
    """
    
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
    """load_player_action_details: loads the guesses and matches, and updates 
    them during a card action initiated by the user

    Args:
        card_handler_dict (_type_): main gameplay details dictionary
        action_turtles (_type_): list of turtle instances representing guesses 
                                 and matches
        column_value (_type_): used for the position adjustment of the score
                               details

    Returns:
        list: list of action turtles
    """
    
    if action_turtles:
        update_action_turtles(action_turtles,card_handler_dict)         
    else:
        guesses_key = customize_turtle_text(
            'Guesses', size=12, goto=(190, column_value-50))       
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
    """load_score_board: loads the scoreboard in the start of the game. Resets
    the old scores and updates the scoreboard in th end of the game.

    Args:
        players_dict (_type_): _description_
        score_turtles (_type_): _description_
    """
    
    #resets old scores to update with latest scores
    if score_turtles:
        card_utils.reset_turtle(score_turtles)

    score_card_title = customize_turtle_text('Score board', size=12, 
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
    
def customize_turtle_text(text, size, goto, font = 'Arial'):
    """customize_turtle_text: customizes the positon and other properties of a
    turtle text

    Args:
        text (_type_): text to display
        size (_type_): size of the text
        goto (_type_): position of the text

    Returns:
        turtle
    """

    t = turtle.Turtle()
    t.hideturtle()
    t.up()
    t.speed(10)
    t.penup()
    t.color('white')
    t.goto(goto)
    t.write(text, move=False, align='left', font=(font, size, 'bold'))
    
    return t
    
def get_game_title(turtle_, is_small=False):
    """get_game_title: adds the game splash art/ title to the play button

    Args:
        turtle_ (_type_): turtle representing the play button
        is_small (bool, optional): will be used on the card deck menu if small 
        is True Defaults to False.
    """

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