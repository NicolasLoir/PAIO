#!env python3
"""
HackaGames - Game - Single421 
"""
import os, sys

from . import engine

sys.path.insert(1, os.path.join(sys.path[0], '..'))
import hackapy as hg
from hackapy import element

class GameTTT(hg.AbsSequentialGame):

    # Constructor
    def __init__(self, mode="classic"):
        super().__init__(2)
        self.mode= mode

    # Game interface :
    def initialize(self):
        if self.mode == "ultimate" :
            self.grid= engine.Ultimate()
        else :
            self.grid= engine.Classic()
        self.count= 4
        return element.Gamel( self.grid.name() )

    def playerHand( self, iPlayer ):
        # Return the game elements in the player vision (an AbsGamel)
        return self.grid.status()

    def applyPlayerAction( self, iPlayer, action ):
        # Apply the action choosen by the player iPlayer. return a boolean at True if the player terminate its actions for the current turn.
        ok= self.grid.apply( iPlayer, action )
        if ok or self.count < 1 :
            self.count= 4
            return True
        self.count-= 1
        return False

    def isEnded( self ):
        # must return True when the game end, and False the rest of the time.
        return self.grid.isEnded()

    def playerScore( self, iPlayer ):
        # If winning
        if self.grid.isWinning(iPlayer) :
            return 1
        # get openent number
        iOponent= 1
        if iPlayer == 1 :
            iOponent= 2
        # if loosing
        if self.grid.isWinning(iOponent) :
            return -1
        # else
        return 0
