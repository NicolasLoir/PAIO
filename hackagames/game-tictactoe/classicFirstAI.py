#!env python3
"""
First TicTacToe player 
"""
import sys, os, random
import matplotlib.pyplot as plt

# Local HackaGame:
sys.path.insert(1, os.path.join(sys.path[0], '..'))
import hackapy as hg


def mainNetwork():
    print('let\'s go... Network')
    player= PlayerRandom()
    results= player.takeASeat()
    print( f"Average: { float(sum(results))/len(results) }" )
    plotResults(results)

def mainLocal():
    print('let\'s go... Local')


class PlayerRandom( hg.AbsPlayer ) :

    # PLayer interface :
    def wakeUp(self, playerId, numberOfPlayers, gameConf):
        mode, game= tuple( gameConf.type().split("-"))
        assert( game == 'TicTacToe' and mode == 'Classic' )
        # Initialize the grid
        self.grid= {
            line: [0 for i in range(4) ]
            for line in ["A", "B", "C"]
        }
        self.end= 0
        self.sign= [ ' ', 'x', 'o' ]
        self.id= playerId
        self.opo= 1
        if playerId == 1 :
            self.opo= 2
        # Verbose:
        print( f'---\nwake-up player-{playerId} ({numberOfPlayers} players)')
        print( gameConf )
    
    def info(self, line):
        position, value= tuple( line.split(": ") )
        abs, ord= tuple( position.split("-") )
        return abs, int(ord), int(value)
    
    def perceive(self, gameState):
        # Update the grid:
        for elt in gameState.children() :
            self.grid[elt.type()]= [0] + elt.attributes()
        # Verbose
        print( f"player: {self.sign[self.id]}" )
        self.printTTT()
    
    def printTTT(self) :
        abss= self.grid.keys()
        ords= range(1, len(abss)+1)
        s= '  '
        for abs in abss :
            s+= ' '+ abs
        print(s)
        for ord in ords :
            s= str(ord) +' '
            for abs in abss :
                s+= ' '+ self.sign[ self.grid[abs][ord] ]
            print(s)

    def actions(self) :
        actions= []
        for abs in ['A', 'B', 'C'] :
            for ord in [1, 2, 3] :
                if self.grid[abs][ord] == 0 :
                    actions.append( f"{abs}-{ord}" )
        return actions

    def decide(self):
        # Get all actions
        actions= self.actions()
        # Select the most 
        maxValue= self.testAction( actions[0] )
        selected= [ actions.pop(0) ]
        for a in actions :
            value= self.testAction(a)
            if value == maxValue :
                selected.append(a)
            elif value > maxValue :
                selected= [a]
                maxValue= value

        action= random.choice( selected )
        print( f'Action: {action}' )
        return action
    
    def testAction(self, a):
        abs, ord= tuple( a.split('-') )
        ord= int(ord)
        self.grid[abs][ord]= self.id
        if self.isWinning( self.id ) :
            return 1
        self.grid[abs][ord]= self.opo
        if self.isWinning( self.opo ) :
            return 0
        self.grid[abs][ord]= 0
        return -1
    
    def isWinning(self, playerId) :
        win= False
        for abs in ["A", "B", "C"]:
            win= win or ( self.grid[abs][1] == playerId and self.grid[abs][2] == playerId and self.grid[abs][3] == playerId )
        for ord in [1, 2, 3]:
            win= win or ( self.grid['A'][ord] == playerId and self.grid['B'][ord] == playerId and self.grid['C'][ord] == playerId )
        win= win or ( self.grid['A'][1] == playerId and self.grid['B'][2] == playerId and self.grid['C'][3] == playerId )
        win= win or ( self.grid['A'][3] == playerId and self.grid['B'][2] == playerId and self.grid['C'][1] == playerId )
        return win

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
    if len(sys.argv) > 1 and sys.argv[1] == 'local' :
        mainLocal()
    else :
        mainNetwork()
