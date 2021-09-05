# -*- coding: utf-8 -*-
from math import log


def compute_cost(rank, total):
    return log(rank * log(total))


def create_cost_map(tokens):
    total = len(tokens)
    costs = list(map(lambda x: compute_cost(x, total), range(1, total+1)))
    cost_map = dict(zip(tokens, costs))
    return cost_map
