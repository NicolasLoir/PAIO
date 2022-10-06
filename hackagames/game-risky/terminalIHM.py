#!env python3
"""
HackaGame player interface 
"""
import sys, os
sys.path.insert(1, os.path.join(sys.path[0], '..'))

import hackapy as hg
import gameEngine as game

class RiskyPlayer(hg.AbsPlayer) :
    # Conscructor :
    def __init__(self, clear= False):
        self.clear= clear

    # Player interface :
    def wakeUp(self, playerId, numberOfPlayers, gameConf):

        print( f'---\nwake-up player-{playerId} ({numberOfPlayers} players)')
        self.board= hg.Board().setFrom( gameConf )
        self.viewer= game.ViewerTerminal( self.board )

    def perceive(self, gameState):
        if self.clear :
            os.system("clear")
        self.board.setFrom( gameState )
        self.viewer.print()
    
    def decide(self):
        action = input('Enter your action: ')
        return action
    
    def sleep(self, result):
        print( f'---\ngame end\nresult: {result}')
