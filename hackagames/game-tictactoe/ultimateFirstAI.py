#!env python3
"""
First TicTacToe player 
"""
import sys, os, random
import matplotlib.pyplot as plt

# Local HackaGame:
sys.path.insert(1, os.path.join(sys.path[0], '..'))
import hackapy as hg

def main():
    print('let\'s go...')
    player= PlayerRandom()
    results= player.takeASeat()
    print( f"Average: { float(sum(results))/len(results) }" )
    plotResults(results)

class PlayerRandom( hg.AbsPlayer ) :

    # PLayer interface :
    def wakeUp(self, playerId, numberOfPlayers, gameConf):
        mode, game= tuple( gameConf.type().split("-"))
        assert( game == 'TicTacToe' and mode == 'Ultimate' )
        # Initialize the grid
        self.grid= {
            line: [0 for i in range(10) ]
            for line in ["A", "B", "C", "D", "E", "F", "G", "H", "I"]
        }
        self.end= 0
        self.sign= [ ' ', 'x', 'o', '-' ]
        self.id= playerId
    
    def info(self, line):
        position, value= tuple( line.split(": ") )
        abs, ord= tuple( position.split("-") )
        return abs, int(ord), int(value)
    
    def perceive(self, gameState):
        # Get the elements
        for elt in gameState.cells() :
            if elt.type() in ["A", "B", "C", "D", "E", "F", "G", "H", "I"] :
                self.grid[elt.type()]= [0] + elt.attributes()
            elif elt.type() == "targets" :
                self.targets= elt.attributes()
        # Verbose:
        print( f"player: {self.sign[self.id]}" )
        self.printTTT()
        print( f"targets: {self.targets}" )
    
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

    def subGrid(self, i):
        if i in [1, 4, 7] :
            abss= [ "A", "B", "C" ]
        elif i in [2, 5, 8] :
            abss= [ "D", "E", "F" ]
        else :
            abss= [ "G", "H", "I" ]
        if i in [1, 2, 3] :
            ords= range(1, 4)
        elif i in [4, 5, 6] :
            ords= range(4, 7)
        else :
            ords= range(7, 10)
            
        return abss, ords
    
    def actions(self) :
        actions= []
        for iGrid in self.targets :
            abss, ords= self.subGrid( iGrid )
            for abs in abss :
                for ord in ords :
                    if self.grid[abs][ord] == 0 :
                        actions.append( f"{abs}-{ord}" )
        return actions

    def decide(self):
        action= random.choice( self.actions() )
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
