#!env python3
"""
First 421 player 
"""
from re import A
import sys, os, random
import matplotlib.pyplot as plt
import json


def verbose( aString ):
    pass

# Local HackaGame:
sys.path.insert(1, os.path.join(sys.path[0], '..'))
import hackapy as hg

def main():
    print('let\'s go...')
    player= Player()
    results= player.takeASeat()
    
    print( f"Average: { float(sum(results))/len(results) }" )
    # plotResults(results)

class Player( hg.AbsPlayer ) :

    def __init__(self):
        super().__init__()
        self.actions= []
        for a1 in ['keep', 'roll']:
            for a2 in ['keep', 'roll']:
                for a3 in ['keep', 'roll']:
                    self.actions.append( a1+'-'+a2+'-'+a3 )
        self.alpha= 0.1 #learning rate: the rate at which the AI agent should learn
        self.gamma= 0.99 #discount factor for future rewards
        self.epsilon= 0.1 #the percentage of time when we should take a random aciton
        self.values= { 'init': {'go': 0.0}, 'end': {'sleep': 0.0} }
        if os.path.isfile("values421.json") :
            f= open("values421.json", 'r')
            self.values= json.load(f)
            f.close()
        
    def __del__(self):
        out_file = open("values421.json", "w")
        json.dump( self.values, out_file, indent= 2)
        out_file.close()

    # Player interface :
    def wakeUp(self, playerId, numberOfPlayers, gameConf):
        #print( f'---\nwake-up player-{playerId} ({numberOfPlayers} players)')
        self.state= 'init'
        self.action= 'go'
        #print( gameConf )

    def perceive(self, gameState):
        # record the last state
        self.lastState= self.state
        # Read game elements
        elements= gameState.children()
        self.horizon= elements[0].attribute(0)
        self.dices= elements[1].attributes()
        
        self.state= f'{self.horizon}{self.dices}'
        verbose(f'State: {self.state}')
        # Udate values
        self.updateValues( self.lastState, self.action, self.state, 0 )
    
    # Qlearning:
    def updateValues( self, lastState, action, newState, reward ):
        print(f'self.state: {self.state}')
        print(f'lastState: {lastState}')
        print(f'action: {action}')
        print(f'newState: {newState}')
        print(f'reward: {reward}')
        if newState not in self.values :
            self.values[newState]= { a:0.0 for a in self.actions }
        bestAction= self.bestAction(newState)
        print(f'bestAction: {bestAction}')
        self.values[lastState][action]= (1-self.alpha)*self.values[lastState][action]
        self.values[lastState][action]+= self.alpha*( reward + self.gamma * self.values[newState][bestAction] )

    def bestAction( self, state ):
        bestA= list(self.values[state].keys())[0]
        for a in self.values[state] :
            if self.values[state][a] > self.values[state][bestA] :
                bestA= a
        return bestA   

    def decide(self):
        # continue playing
        if random.random() < self.epsilon :
            self.action= random.choice( self.actions )
            verbose( f'Action: {self.action} (R)' )
        else :
            self.action= self.bestAction( self.state )
            verbose( f'Action: {self.action}  (B)' )
        return self.action
    
    def sleep(self, result):
        # update the value with final score:
        print(f'methode sleep, valeur de self.action: {self.action}')
        self.updateValues( self.state, self.action, 'end', result )
        verbose( f'--- Results: {str(result)}' )
        # save:

    
    
         

def plotResults(results, scope= 500):
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
