import turtle, os 

class Card:
    def __init__(self, index, name):
        self.index = index
        self.turtle = turtle.Turtle()
        self.turtle.up()
        self.turtle.speed(5)
        self.turtle.shape(os.path.join(os.path.join(os.getcwd(), 'assets'),
                                       'card_back.gif'))
        if index < 4:
            self.turtle.setposition(-200 + 100*index, 200)
        elif index >= 4 and index < 8:
            self.turtle.setposition(-600 + 100*index, 45)
        else:
            self.turtle.setposition(-1000 + 100*index, -110)
        self.name = name

       
    def reset_card(self):
        self.turtle.shape(os.path.join(os.path.join(os.getcwd(), 'assets'),
                                  'card_back.gif'))
        
    def flip_card(self):
        self.turtle.shape(os.path.join(os.path.join(os.getcwd(), 'assets'),
                                  self.name))
    
    def hide_card(self):
        self.turtle.hideturtle()
        