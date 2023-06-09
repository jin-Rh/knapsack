import numpy as np
import pandas as pd
from collections import deque
import random

# Constants
# max weight of the knapsack
MAX_WEIGHT = 1000
# max number of iterations
MAX_ITER = 20
# tabu list size
TABU_SIZE = 20
# item total
MAX_ITEMS = 100

# read data from a file and check the first few items
data = pd.read_csv('knapsack.csv')

# returns the list of tuples with a weight and value pair
def all_items():
    items = []
    for i in range(MAX_ITEMS):
        weight = data.loc[i].item_weights
        value = data.loc[i].item_values
        items.append((weight, value))
    print('All items for the knapsack algorithms (weight, value)= \n', items)
    return items


def is_feasible(items, config):
    if calculate_weight(items, config) <= MAX_WEIGHT:
        return True

    return False


# calculate the total value of a knapsack configuration
def calculate_value(items, config):
    total_value = 0
    for i, item in enumerate(items):
        if config[i] == 1:
            total_value += item[1]
    return total_value


# calculate the total weight of a knapsack configuration
def calculate_weight(items, config):
    total_wt = 0
    for i, item in enumerate(items):
        if config[i] == 1:
            total_wt += item[0]
    return total_wt


# generate a random initial configuration
def create_initial_config(n):
    return [random.randint(0, 1) for _ in range(n)]


# generate neighbouring configurations - selected 1 not 0
def create_neighbours(curr_config):
    neighbours = []
    for i in range(len(curr_config)):
        current = curr_config.copy()
        current[i] = 1 - current[i]
        neighbours.append(current)
    #         print('new neighbours = ', neighbours)
    return neighbours


def find_best_neighbours(items, current_config, tabu_list):
    neighbours = create_neighbours(current_config)
    best_neighbour = current_config
    best_value = calculate_value(items, current_config)

    for neighbour in neighbours:
        if neighbour not in tabu_list:
            neighbour_value = calculate_value(items, neighbour)
            neighbour_weight = calculate_weight(items, neighbour)
            if neighbour_weight <= MAX_WEIGHT and neighbour_value > best_value:
                best_neighbour = neighbour
                best_value = neighbour_value
    return best_neighbour, best_value


# tabu search
def knapsack_tabu(items, max_wt, max_iter, tabu_size):
    # find the current knapsack items
    curr_conf_list = create_initial_config(len(items))
    current_weight = calculate_weight(items, curr_conf_list)
    curr_val = calculate_value(items, curr_conf_list)
    # set variables for best solution
    best_conf = curr_conf_list
    best_val = curr_val
    tabu_list = deque()
    iters = 0
    while iters < max_iter:
        best_neighbour, best_val = find_best_neighbours(items, curr_conf_list, tabu_list)
        # any neighbour with better value
        if best_val > curr_val:
            curr_conf_list = best_neighbour
            curr_val = best_val
            if best_val > calculate_value(items, best_conf):
                best_conf = best_neighbour
        # add the neighbour onto tabu list
        tabu_list.append(best_neighbour)
        if len(tabu_list) > tabu_size:
            tabu_list.pop()
        iters += 1
    final_val = calculate_value(items, best_conf)
    # returns a tuple of binary list, value, weight
    return best_conf, final_val, current_weight
