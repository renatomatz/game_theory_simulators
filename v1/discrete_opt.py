import numpy as np

from pprint import pprint
from scipy.optimize import minimize


def two_player_payoff(x, y, p, max_y=False):
    return -np.sum([
        p[i, j][int(max_y)]*x[i]*y[j]
        for i in range(len(x)) for j in range(len(y))
    ])


def n_player_payoff(p_strat, all_strats, payoffs, player):
    ex_p = payoffs[..., player]
    for i, strat in enumerate(all_strats):
        if i == player:
            ex_p = ex_p * p_strat
        else:
            ex_p = ex_p * strat
    return -np.sum(ex_p)


def two_players(payoffs, learning_rate=0.01, n_iter=1000, verbose=False):
    
    x = np.ones(payoffs.shape[0]) / payoffs.shape[0]
    y = np.ones(payoffs.shape[1]) / payoffs.shape[1]
    
    x_log = np.array([x])
    y_log = np.array([y])
    
    y_plays = True
    
    for _ in range(n_iter):
        
        if verbose:
            print("x"*(1-y_plays) + "y"*y_plays, ": turn")
        
        res = minimize(
            two_player_payoff,
            x*(1 - y_plays) + y*y_plays,
            method="SLSQP",
            bounds=np.array([(0, 1), (0, 1)]),
            constraints={
                "type": "eq",
                "fun": lambda inputs: 1.0 - np.sum(inputs),
            },
            args=((
                x*y_plays + y*(1-y_plays),
                payoffs, 
                y_plays,
            ))
        )
        
        opt = res.x
        
        if verbose:
            print("optimal move: ", opt)
        
        if y_plays:
            y = y + (opt - y)*learning_rate
            y /= np.sum(y)
            y_log = np.append(y_log, np.array([y]), axis=0)
        else:
            x = x + (opt - x)*learning_rate
            x /= np.sum(x)
            x_log = np.append(x_log, np.array([x]), axis=0)

        
        y_plays = not y_plays
        
    return {
        "x_log": x_log,
        "y_log": y_log,
        "final_res": {
            "p1": x,
            "p2": y
        }
    }


def find_best_strat(payoffs, learning_rate=0.01, n_iter=1000, verbose=False, init_method="equal"):
    
    assert payoffs.shape[-1] == (len(payoffs.shape) - 1)
    
    if init_method == "equal":
        strategies = [
            np.ones(n) / n
            for n in payoffs.shape
        ][:-1]
    elif init_method == "random":
        strategies = [
            np.random.randn(n)
            for n in payoffs.shape
        ][:-1]
        
        strategies = [
            row / np.sum(row)
            for row in strategies
        ]
        
    log = {i: np.array([strategies[i]]) for i in range(payoffs.shape[-1])}
    
    for _ in range(n_iter):
        
        opt = []
        
        for i in range(payoffs.shape[-1]):
        
            if verbose:
                print(f"Player {i}'s turn")

            res = minimize(
                n_player_payoff,
                strategies[i],
                method="SLSQP",
                bounds=np.array([(0, 1)]*len(strategies[i])),
                constraints={
                    "type": "eq",
                    "fun": lambda inputs: 1.0 - np.sum(inputs),
                },
                args=((
                    strategies,
                    payoffs, 
                    i,
                ))
            )
            
            if not res.success:
                raise RuntimeError("Optimization Error")

            opt.append(res.x)

        if verbose:
            print("optimal moves: ", opt)

        for i in range(payoffs.shape[-1]):

            strategies[i] = (
                strategies[i]
                + (opt[i] - strategies[i])*learning_rate
            )

            strategies[i] /= np.sum(strategies[i])
                
            log[i] = np.append(log[i], np.array([strategies[i].copy()]), axis=0)
        
    return strategies, log
