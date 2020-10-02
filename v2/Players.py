"""
"""
from typing import Any

import numpy as np

from scipy.optimize import minimize


class Players:
    """
    """

    cache: Any
    journal: dict

    strategies: list
    players: list

    def __init__(self, journal=True):
        """
        """
        raise NotImplementedError()

    def optimal(self, env, player):
        """
        """
        raise NotImplementedError()

    def optimize(self, env, player, cache=False):
        """
        """
        raise NotImplementedError()
        
    def update(self):
        """
        """
        raise NotImplementedError()

    def clear_cache(self):
        """
        """
        raise NotImplementedError()


class NNMatrixPlayers(Players):
    """
    """

    learning_rate: float

    def __init__(self, 
                 n_players, 
                 n_strats, 
                 init_method="equal", 
                 learning_rate=0.01,
                 journal=True):
        """
        """

        assert n_players == len(n_strats)

        self.players = list(range(n_players))

        self.journal = {i:list() for i in range(n_players)} \
            if journal else None
        
        if init_method == "equal":
            self.strategies = {
                i: np.ones(n) / n
                for i, n in enumerate(n_strats)
            }
        elif init_method == "random":
            self.strategies = {
                i: np.random.randn(n)
                for i, n in enumerate(n_strats)
            }
            
            self.strategies = {
                i: row / np.sum(row)
                for i, row in enumerate(self.strategies)
            }

        self.learning_rate = learning_rate

        self.clear_cache()

    @classmethod
    def from_payoff_matrix(cls, payoffs, *args, **kwargs):
        return cls(payoffs.shape[-1], 
                   payoffs.shape[:-1], 
                   *args, **kwargs)

    @staticmethod
    def n_player_payoff(p_strat, all_strats, payoffs, player):
        """
        """
        ex_p = payoffs[..., player]
        for i, strat in all_strats.items():
            if i == player:
                ex_p = ex_p * p_strat
            else:
                ex_p = ex_p * strat
        return -np.sum(ex_p)

    def optimal(self, env, player):
        return minimize(
            NNMatrixPlayers.n_player_payoff,
            self.strategies[player],
            method="SLSQP",
            bounds=np.array([(0, 1)]*len(self.strategies[player])),
            constraints={
                "type": "eq",
                "fun": lambda inputs: 1.0 - np.sum(inputs),
            },
            args=((
                self.strategies,
                env.payoffs, 
                player,
            ))
        )

    def optimize(self, env, player, cache=False):
        res = self.optimal(env, player)

        if not res.success:
            raise RuntimeError("Optimization Error")

        new_strat = self.strategies[player]

        new_strat = (
            new_strat
            + (res.x - new_strat)*self.learning_rate
        )
        new_strat /= np.sum(new_strat)

        if cache:
            self.cache[player] = new_strat
        else:
            self.strategies[i] = new_strat

        if self.journal is not None:
            self.journal[player].append(new_strat)

        return player

    def update(self):
        self.strategies.update(self.cache)
        self.clear_cache()

    def clear_cache(self):
        self.cache = {}
