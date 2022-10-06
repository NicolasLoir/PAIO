#!env python3
"""
HackaGame player interface 
"""
import sys, os
sys.path.insert(1, os.path.join(sys.path[0], '..'))

import hackapy.cmd as cmd
import hackapy.player as pl

class TTTPlayer(pl.AbsPlayer) :
    # PLayer interface :
    def wakeUp(self, playerId, numberOfPlayers, gameConf):
        mode, game = tuple( gameConf.type().split("-"))
        print( f'---\nwake-up player-{playerId} ({numberOfPlayers} players)')
        print( game + ' ' + mode )
        assert( game == 'TicTacToe' and mode in ['Classic', 'Ultimate'] )
        self.mode= mode
        # Get Classic or Ultimate config:
        abss= ["A", "B", "C"]
        ordss= range(4)
        if mode == "Ultimate" :
            abss= ["A", "B", "C", "D", "E", "F", "G", "H", "I"]
            ordss= range(10)
        # Initialize the grid
        self.grid= {
            line: [0 for i in ordss ]
            for line in abss
        }
        self.end= 0
        self.sign= [ ' ', 'x', 'o' ]
        self.id= playerId

    def info(self, line):
        position, value= tuple( line.split(": ") )
        abs, ord= tuple( position.split("-") )
        return abs, int(ord), int(value)
    
    def perceive(self, gameState):
        # print the grid:
        os.system("clear")
        print( f"player: {self.sign[self.id]}" )
        # Get the elements
        for elt in gameState.children() :
            if elt.type() in ["A", "B", "C", "D", "E", "F", "G", "H", "I"] :
                self.grid[elt.type()]= [0] + elt.attributes()
            elif elt.type() == "targets" :
                self.targets= elt.attributes()
                print( '> targets: ' + str(self.targets) )
        # and print
        self.printTTT()
    
    def printTTT(self) :
        abss= self.grid.keys()
        ords= range(1, len(abss)+1)
        s= '  '
        for abs in abss :
            if abs in ['D', 'G']:
                s+= '  '
            s+= ' '+ abs
        print(s)

        for ord in ords :
            if ord in [4, 7] :
                print( "  -------|-------|-------" )
            s= str(ord) +' '
            for abs in abss :
                if abs in ['D', 'G']:
                    s+= ' |'
                s+= ' '+ self.sign[ self.grid[abs][ord] ]
            print(s)
        if self.mode == "Ultimate" :
            print( f"target: {self.targets}" )
    
    def decide(self):
        action = input('Enter your action: ')
        return action
    
    def sleep(self, result):
        print( f'---\ngame end\nresult: {result}')
