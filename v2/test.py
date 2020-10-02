from Environment import NNMatrix
from Players import NNMatrixPlayers
from Game import NNMatrixGame
from sample_games import battle_of_sexes

import numpy as np

env = NNMatrix(battle_of_sexes)
players = NNMatrixPlayers.from_payoff_matrix(battle_of_sexes)
game = NNMatrixGame(
    env=env,
    players=players
)
game.run()
print("Done")