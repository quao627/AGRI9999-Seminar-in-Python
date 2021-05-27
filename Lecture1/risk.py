# -*- coding: utf-8 -*-
"""
Risk Simulation:
    Risk is a popular boardgame where players aim to conqure all territories 
    by building an army and engaging in battles. A battle consists of the 
    attacker and the defender and is decided by comparing the dice they 
    rolled.
    In each battle, the attacker can roll up to 3 dice and the defender can 
    roll up to 2 dice. To decide a battle, first compare the highest die each
    of them rolled. If the attacker's die is higher than the defender's die,
    then the defender loses one military unit. Otherwise the attacker
    loses one military unit. (the defender wins if there is a tie.) Then, 
    compare the second highest die following the same rule.
    In this exercise, we will use two approaches to implement the monte carlo
    simulation that estimates the expected number of rounds each player wins 
    in a battle.
"""

import random
import time
import numpy as np


'''
Probablistic Model:
    Weak Law of Large Numbers:
        lim P(|sample mean - actual mean| >= eps) goes to 0 as sample size
        goes to infinity.
'''
def for_approach(num_iterations):
    start_time = time.time()
    
    attacker_sum = 0
    defender_sum = 0
    dice_options = [i for i in range(1, 7)]
    for i in range(num_iterations):
        attacker_gain = 0
        defender_gain = 0
        attacker = random.choices(dice_options, k=3)
        defender = random.choices(dice_options, k=2)
        attacker.sort(reverse=True)
        defender.sort(reverse=True)
        
        if attacker[0] > (defender[0] + 0.5):
            attacker_gain += 1
        else:
            defender_gain += 1
        
        if attacker[1] > (defender[1] + 0.5):
            attacker_gain += 1
        else:
            defender_gain += 1
            
            
        '''
        attacker_gain = (int(attacker[0] > defender[0] + 0.5) + 
                        int(attacker[1] > defender[1] + 0.5))
        defender_gain = 2 - attacker_gain
        '''
        
        attacker_sum += attacker_gain
        defender_sum += defender_gain
    
    end_time = time.time()
       
    print("For loop approach:") 
    print("On average attacker makes {} wins while defender makes {} wins"
          .format(attacker_sum/num_iterations, defender_sum/num_iterations))
    print("It takes {} seconds to run this program. \n".format(end_time - start_time))


'''
Advanced: Numpy Approach (optional)
'''
def numpy_approach(num_iterations):
    start_time = time.time()
    
    attacker_matrix = np.random.randint(low=1, high=7, size=(3, num_iterations))
    attacker_matrix.sort(axis=0)
    attacker_matrix = attacker_matrix[1:, :]
    
    defender_matrix = np.random.randint(low=1, high=7, size=(2, num_iterations))
    defender_matrix.sort(axis=0)
    defender_matrix = defender_matrix + 0.5
    
    attacker_sum = sum(sum(attacker_matrix > defender_matrix))
    defender_sum = sum(sum(attacker_matrix < defender_matrix))
        
    
    end_time = time.time()
    
    print("Matrix approach:") 
    print("On average attacker makes {} wins while defender makes {} wins"
          .format(attacker_sum/num_iterations, defender_sum/num_iterations))
    print("It takes {} seconds to run this program.".format(end_time - start_time))
    
if __name__ == '__main__':
    num_iterations = 10**6
    for_approach(num_iterations)
    numpy_approach(num_iterations)




        