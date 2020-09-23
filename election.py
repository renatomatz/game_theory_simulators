#!/usr/bin/env python
# coding: utf-8

# In[20]:


from pprint import pprint
import numpy as np
from itertools import combinations_with_replacement


# In[51]:


def get_candidate_payoffs(candidates, voters):
    votes = np.zeros(len(candidates))
    for voter in voters:
        choice, distance = None, np.inf
        for i, candidate in enumerate(candidates):
            can_dist = np.sqrt(np.sum((voter - candidate)**2))
            if can_dist < distance or (can_dist == distance and np.random.random() >= 0.5):
                choice, distance = i, can_dist
        votes[choice] += 1
    #print(f"Candidate Positions: {candidates}")
    #print(f"Votes: {votes}")
    return votes

def get_strategy_payoffs(action_set, n_candidates, n_positions, voters_per_candidate, voter_gen, payoff_func):
    
    possible_candidates = combinations_with_replacement(
        combinations_with_replacement(action_set, n_positions), 
        n_candidates
    )

    voters = voter_gen((voters_per_candidate*n_candidates, n_positions))
    action_dict = {action:0 for action in combinations_with_replacement(action_set, n_positions)}

    for candidate_positions in possible_candidates:
        res = get_candidate_payoffs(candidate_positions, voters)
        for action, res in zip(candidate_positions, res):
            action_dict[action] += res
            
    # print(f"Outcomes: {action_dict}")
            
    action_dict = {action: payoff for action, payoff 
                   in zip(action_dict.keys(), payoff_func(
                       np.array([*action_dict.values()])
                   ))}
    
    return action_dict

def proportionate(votes):
    return votes / votes.sum()

def winner_takes_it_all(votes):
    winner = (votes == votes.max()).astype(int)
    return winner / winner.sum()


# In[56]:


# action_set = np.arange(0, 1.1, 0.1)
action_set = np.array([0, 1/2, 1])

res = get_strategy_payoffs(
    action_set,
    3,
    2,
    50,
    np.random.random,
    proportionate
)
pprint(res)
# Keep positions of other players
