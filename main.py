import pickle
from os import path
from game import Game
if path.exists('data.pickle'):
    with open('data.pickle', 'rb') as f:
        game = pickle.load(f)
else:
    game = Game()
qa = game.run()
pass