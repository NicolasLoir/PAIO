#!env python3
"""
Script MDP 421 
"""
import os, sys

sys.path.insert(1, os.path.join(sys.path[0], '..'))
import hackapy as hg
from . import engine as ge

class Game(hg.AbsGame) :
    def __init__(self, port=1400):
        super().__init__(2, port)

    def play(self):
        engine= ge.Engine421()
        score= 0.0
        self.scoreRef= -1
        engine.initialize()
        self.wakeUpPlayers('Battle421')
        while not engine.isEnd() :
            action= self.activatePlayer( 1, self.hackaState(engine) )
            score= engine.step( action )

        self.scoreRef= score
        score= 0.0
        engine.initialize()
        while not engine.isEnd() :
            action= self.activatePlayer( 2, self.hackaState(engine) )
            score= engine.step( action )
        
        diffScore= self.scoreRef-score
        if diffScore > 0 :
            diffScore= 1
        elif diffScore < 0 :
            diffScore= -1
        
        self.sleepPlayer( 1, self.hackaState(engine), diffScore )
        self.sleepPlayer( 2, self.hackaState(engine), -diffScore )

    def hackaState(self, engine):
        return f'S: {(int)(self.scoreRef)} H: {engine.turn()} DICES: '+ ' '.join([ str(d) for d in engine.dices() ])
