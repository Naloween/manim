from manim import *
from manim.player import *

def sequence_1(player: Player):
    player.play(Write(Text("My presentation!\nNathanaël Haas"), run_time=3))

def sequence_2(player: Player):
    player.clear()
    
    square = Square(name="square")  # create a square
    square.rotate(PI / 4)  # rotate a certain amount
    
    player.play(Create(square))

def sequence_3(player: Player):
    square =  player.find_mobj_by_name("square")
    circle = Circle(name="circle")  # create a circle
    circle.set_fill(PINK, opacity=0.5)  # set color and transparency

    player.play(Transform(square, circle))
    player.play(FadeOut(square))


def sequence_4(player: Player):
    player.clear()
    player.play(Write(Text("Thank you for you attention!")))



sequences = [sequence_1, sequence_2, sequence_3, sequence_4]

player = Player(sequences, fullscreen=True)
player.run()