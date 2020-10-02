"""
"""
import numpy as np


class Environment:

    def __init__(self):
        raise NotImplementedError()

    def update(self):
        raise NotImplementedError()


class NNMatrix(Environment):
    """
    """

    payoffs: np.ndarray
    n_players: int
    n_strats: np.ndarray

    def __init__(self, payoffs):
        """
        """

        assert isinstance(payoffs, np.ndarray)

        self.payoffs = payoffs
        self.n_strats, self.n_players = payoffs.shape[:-1], payoffs.shape[-1]

    def update():
        pass
