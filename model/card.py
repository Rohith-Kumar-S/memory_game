"""
CS 5001
Rohith Kumar Senthil Kumar
Fall 2024

A class representing a Card for the memory game
"""

import turtle, os 

class Card:
    """This class is a cutomized variant of a turtle, with a shape of a card  
    """
    
    def __init__(self, index, name, card_back=''):
        """creates new instance for a Card, sets the position of the card on
        the screen based on the index passed.

        Args:
            index (_type_): index of the card, used for identification
            name (_type_): name of the card, unique value
            card_back (str, optional): sets a custom back side for the card
            if a path is passed. Defaults to ''.
        """
        
        self.index = index
        self.turtle = turtle.Turtle()
        self.turtle.up()
        self.turtle.speed(5)
        self.turtle.shape(os.path.join(os.path.join(os.getcwd(), 'assets'),
                                       'card_back.gif')  if not card_back else\
                                           card_back)
        if index < 4:
            self.turtle.setposition(-207 + 105 * index, 200)
        elif index >= 4 and index < 8:
            self.turtle.setposition(-627 + 105 * index, 45)
        else:
            self.turtle.setposition(-1047 + 105 * index, -110)
        self.name = name

       
    def reset_card(self):
        """reset_card: flips the card back to the back side of the card.
        """
        
        self.turtle.shape(os.path.join(os.path.join(os.getcwd(), 'assets'),
                                  'card_back.gif'))
        
    def flip_card(self):
        """flip_card: flips the card to reveal the other side of the card
        """
        
        self.turtle.shape(os.path.join(os.path.join(os.getcwd(), 'assets'),
                                  self.name))
    
    def hide_card(self):
        """hide_card: hides the card after a right choice was made
        """
        
        self.turtle.hideturtle()