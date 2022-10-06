#!env python3
import sys, os
import numpy as np

sys.path.insert(1, os.path.join(sys.path[0], '..'))
from gameEngine.engine import Engine421 as g421

def main():
    iaQlearning = Qlearning421()
    iaQlearning.train()

class Qlearning421() :

    def __init__( self ):
        self.initialize()

    def initialize(self):
        if os.path.exists('qvalue.npy'):
            self.q_values = np.load('qvalue.npy')
        else:
            self.nb_horizon = 2 #il reste 0, 1 ou 2 tours. Pour l'instant je ne prends pas en compte ce facteur
            de1 = 6 #6 possibilité
            de2 = 6 #6 possibilité
            de3 = 6 #6 possibilité
            nb_actions = 8 # keep-keep-keep
                        # roll-keep-keep keep-roll-keep keep-keep-roll
                        # keep-roll-roll roll-keep-roll roll-roll-keep
                        # roll-roll-roll
            self.q_values = np.zeros((de1, de2, de3, nb_actions))
        # self.q_values = np.load('qvalue.npy')
        self.epsilon = 0.9 #the percentage of time when we should take the best action (instead of a random action)
        self.discount_factor = 0.9 #discount factor for future rewards
        self.learning_rate = 0.9 #the rate at which the AI agent should learn
        self.jeu = g421()
        self.actions = self.jeu.allActionsStr()

    def train(self, nb_training = 1000000):
        for episode in range(nb_training):
            self.jeu.initialize()
            old_dice = self.jeu.dices() #store the old index


            #choose which action to take (i.e., where to move next)
            action_index = self.get_indice_next_action(old_dice, self.epsilon)

            #perform the chosen action, and transition to the next state
            self.jeu.step(self.actions[action_index])
            new_dice = self.jeu.dices() #store the old index

            #receive the reward for moving to the new state, and calculate the temporal difference
            reward =  self.jeu.score(self.jeu.stateDico())
            old_q_value =  self.q_values[old_dice[0] - 1, old_dice[1] - 1, old_dice[2] - 1, action_index]

            temporal_difference = reward + ( self.discount_factor * np.max( self.q_values[new_dice[0] - 1, new_dice[1] - 1, new_dice[2] - 1]))

            #update the Q-value for the previous state and action pair
            new_q_value = (1 - self.learning_rate) * old_q_value + ( self.learning_rate * temporal_difference)
            self.q_values[old_dice[0] - 1, old_dice[1] - 1, old_dice[2] - 1, action_index] = new_q_value
            # print(f"reward: {reward}, old_q_value: {old_q_value}, new_q_value: {new_q_value}")
        print('Training complete!')
        np.save('qvalue', self.q_values)

    def get_indice_next_action(self, des, epsilon):
        if np.random.random() < epsilon:
            indice_action =  np.argmax(self.q_values[des[0] - 1, des[1] - 1, des[2] - 1])
        else:
            indice_action = np.random.randint(8) #int entre 0 et 7
        return indice_action

    def get_best_action(self, des):
        action_index = self.get_indice_next_action(des, 1.)
        return self.actions[action_index]



if __name__ == '__main__' :
    main()

