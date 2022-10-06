#!env python3
import sys, os
import numpy as np

sys.path.insert(1, os.path.join(sys.path[0], '..'))
from gameEngine.engine import Engine421 as g421

def main():
    iaQlearning = Qlearning421_V2()
    iaQlearning.train()

class Qlearning421_V2() :

    def __init__( self ):
        self.initialize()
    
    def initialize(self):
        # nb_horizon = 2 #il reste 0, 1 ou 2 tours. Pour l'instant je ne prends pas en compte ce facteur
        # de1 = 6 #6 possibilité
        # de2 = 6 #6 possibilité
        # de3 = 6 #6 possibilité
        # nb_actions = 8 # keep-keep-keep 
        #             # roll-keep-keep keep-roll-keep keep-keep-roll 
        #             # keep-roll-roll roll-keep-roll roll-roll-keep
        #             # roll-roll-roll
        # self.q_values = np.zeros((nb_horizon, de1, de2, de3, nb_actions))
        self.q_values = np.load('qvalueV2.npy')
        self.epsilon = 0.9 #the percentage of time when we should take the best action (instead of a random action)
        self.discount_factor = 0.9 #discount factor for future rewards
        self.learning_rate = 0.9 #the rate at which the AI agent should learn
        self.jeu = g421()
        self.actions = self.jeu.allActionsStr()

    def train(self, nb_training = 10000000):
        for episode in range(nb_training):
            self.jeu.initialize()
            first_dice = self.jeu.dices() #store the old index

            number_dice_to_launch_left = 2 #first dice roll

            #choose which action to take (i.e., where to move next)
            first_action_index = self.get_indice_next_action(number_dice_to_launch_left, first_dice, self.epsilon)

            #perform the chosen action, and transition to the next state
            self.jeu.step(self.actions[first_action_index])

            #si le jeu est fini au tour 1, l'action prise est keep-keep-keep
            if (self.actions[first_action_index] == "keep-keep-keep"):
                #receive the reward for moving to the new state, and calculate the temporal difference
                reward =  self.jeu.score(self.jeu.stateDico())
                old_q_value =  self.q_values[number_dice_to_launch_left - 1, first_dice[0] - 1, first_dice[1] - 1, first_dice[2] - 1, first_action_index]
                temporal_difference = reward + ( self.discount_factor * np.max( self.q_values[number_dice_to_launch_left - 1, first_dice[0] - 1, first_dice[1] - 1, first_dice[2] - 1])) - old_q_value

                #update the Q-value for the previous state and action pair
                new_q_value = old_q_value + ( self.learning_rate * temporal_difference)
                self.q_values[number_dice_to_launch_left - 1, first_dice[0] - 1, first_dice[1] - 1, first_dice[2] - 1, first_action_index] = new_q_value
            else:
                number_dice_to_launch_left = 1 #second dice roll
                second_dice = self.jeu.dices()

                second_action_index = self.get_indice_next_action(number_dice_to_launch_left, second_dice, self.epsilon)
                self.jeu.step(self.actions[second_action_index])

                #receive the reward for moving to the new state, and calculate the temporal difference
                reward =  self.jeu.score(self.jeu.stateDico())
                old_q_value_first_dice = self.q_values[1, first_dice[0] - 1, first_dice[1] - 1, first_dice[2] - 1, first_action_index]
                old_q_value_second_dice =  self.q_values[0, second_dice[0] - 1, second_dice[1] - 1, second_dice[2] - 1, second_action_index]
                
                temporal_difference_first_dice = reward + ( self.discount_factor * np.max( self.q_values[1, first_dice[0] - 1, first_dice[1] - 1, first_dice[2] - 1])) - old_q_value_first_dice
                temporal_difference_second_dice = reward + ( self.discount_factor * np.max( self.q_values[0, second_dice[0] - 1, second_dice[1] - 1, second_dice[2] - 1])) - old_q_value_second_dice

                #update the Q-value for the previous state and action pair
                new_q_value_first_dice = old_q_value_first_dice + ( self.learning_rate * temporal_difference_first_dice)
                new_q_value_second_dice = old_q_value_second_dice + ( self.learning_rate * temporal_difference_second_dice)

                self.q_values[1, first_dice[0] - 1, first_dice[1] - 1, first_dice[2] - 1, first_action_index] = new_q_value_first_dice
                self.q_values[0, second_dice[0] - 1, second_dice[1] - 1, second_dice[2] - 1, second_action_index] = new_q_value_second_dice

        print('Training complete!')
        np.save('qvalueV2', self.q_values)

    def get_indice_next_action(self, horizon, des, epsilon):
        if np.random.random() < epsilon:
            indice_action =  np.argmax(self.q_values[horizon - 1, des[0] - 1, des[1] - 1, des[2] - 1])
        else: 
            indice_action = np.random.randint(8) #int entre 0 et 7
        return indice_action
    
    def get_best_action(self, horizon, des):
        action_index = self.get_indice_next_action(horizon, des, 1.)
        return self.actions[action_index]



if __name__ == '__main__' :
    main()

