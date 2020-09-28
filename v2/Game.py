"""
"""
from multiprocessing import Pool
import numpy as np

from Players import Players


class Game:
    """
    """

    env: Environment
    player: Players

    def __init__(self, 
                 env=None, 
                 players=None, 
                 update_strategy=None, 
                 run_opts=None):
        """
        """
        raise NotImplementedError()

    def run(self, n_itter=100, n_jobs=1):
        """
        """
        raise NotImplementedError()


class NNMatrixGame(Game):
    """
    """

    groups: list

    def __init__(self, 
                 env=None, 
                 players=None, 
                 update_strategy="all", 
                 run_opts=None):

        # TODO: check for env/game compatibility

        self.env=env
        self.players=players
        self.update_strategy=update_strategy
        
        if update_strategy == "groups":

            if (run_opts is None) or ("groups" not in run_opts):
                raise ValueError("if update_strategy is 'groups', you must \
                    specify the groups in the 'groups' key in the run_opts \
                    parameter")

            self.groups = run_opts["groups"]

        self.n_jobs = run_opts.get("n_jobs", 1)

    def run(self, n_iter=100, n_jobs=None, verbose=False):

        for _ in range(n_iter):

            update_groups = []
            if self.update_strategy == "all":
                update_groups = [self.players.players]
            elif self.update_stretegy == "single" 
                update_groups = [[player] for player in self.players.players]
            elif self.update_stretegy == "groups" 
                update_groups = self.groups
            
            for group in update_groups:

                with Pool(processes=self.n_jobs if n_jobs is None else n_jobs) as pool:

                    res = pool.map_async(
                        self.players.optimize,
                        ((self.env, player, True) for player in group),
                        lambda x: print(f"Player {x}'s turn") if verbose \
                            else None
                    )

                [res.wait() for _ in group]

                self.players.update()

        return True
