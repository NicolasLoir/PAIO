#!env python3
"""
First 421 player
"""
import sys, os, random
import matplotlib.pyplot as plt

# Local HackaGame:
sys.path.insert(1, os.path.join(sys.path[0], '..'))
import hackapy as hg
from qlearning import Qlearning421 as iaQlearning421
from qlearningV2 import Qlearning421_V2 as iaQlearning421_V2
from qlearningV3 import Qlearning421_V3 as iaQlearning421_V3


def main():
    actions= []
    for a1 in ['keep', 'roll']:
        for a2 in ['keep', 'roll']:
            for a3 in ['keep', 'roll']:
                actions.append( a1+'-'+a2+'-'+a3 )
    print('let\'s go...')
    player= PlayerRandom(actions)
    results= player.takeASeat()
    print( f"Average: { float(sum(results))/len(results) }" )
    plotResults(results)

class PlayerRandom( hg.AbsPlayer ) :

    def __init__(self, actions):
        super().__init__()
        self.actions= actions

    # Player interface :
    def wakeUp(self, playerId, numberOfPlayers, gameConf):
        print( f'---\nwake-up player-{playerId} ({numberOfPlayers} players)')
        print( gameConf )

    def perceive(self, gameState):
        elements= gameState.children()
        self.horizon= elements[0].attribute(0)
        self.dices= elements[1].attributes()
        if len(elements) == 3 : # ie in duo mode
            self.reference= elements[2].attribute(0)
            print( f'H: {self.horizon} DICES: {self.dices} REF: {self.reference}' )
        else :
            print( f'H: {self.horizon} DICES: {self.dices}' )

    def decide(self):
        # action= random.choice( self.actions )
        # action = "roll-roll-roll"
        # if (self.dices[0] == 4 & self.dices[1] == 2 & self.dices[2] == 1):
        #     action = "keep-keep-keep"
        # elif(self.dices[2] == 1):
        #     action = "roll-roll-keep"
        #     if (self.dices[1] == 1):
        #         action = "roll-keep-keep"
        # elif(self.dices[0] == self.dices[1] & self.dices[0] == self.dices[2] & self.horizon == 0):
        #     action = "keep-keep-keep"
        # elif (self.dices[1] == self.dices[0]-1 & self.dices[2] == self.dices[0]-2 & self.horizon == 0):
        #     action = "keep-keep-keep"
        # print( f'Action: {action}' )

        # iaQlearning = iaQlearning421()
        # action = iaQlearning.get_best_action(self.dices)

        # iaQlearningV2 = iaQlearning421_V2()
        # action = iaQlearningV2.get_best_action(self.horizon, self.dices)

        iaQlearningV3 = iaQlearning421_V3()
        action = iaQlearningV3.get_best_action(self.horizon, self.dices)

        print(f'Des: {self.dices}')
        print( f'Action: {action}' )
        return action

    def sleep(self, result):
        print( f'--- Results: {str(result)}' )

def plotResults(results, scope= 100):
    # Calibrate the scope:
    if len(results) <= scope :
        scope= 1
    # Compute averages avery scope results:
    averageScores= []
    for i in range( scope, len(results)+1 ) :
        averageScores.append( sum(results[ i-scope:i ])/scope )
    # And plot it:
    plt.plot( averageScores )
    plt.ylabel( "scores" )
    plt.show()

# script
if __name__ == '__main__' :
    main()
