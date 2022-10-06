#!env python3
"""
HackaGame - Game - Risky 
"""
import os, sys, random
gamePath= os.path.join(sys.path[0])
sys.path.insert(1, os.path.join(gamePath, '..'))
import hackapy as hg

# Army Attributes
ACTION= 1
FORCE=  2

class GameRisky( hg.AbsSequentialGame ) :

    # Constructor
    def __init__(self, numerOfPlayers= 1, map="board-4" ):
        super().__init__(numerOfPlayers)
        self.map= map
        self.degatMethod= self.degatStochastic
        self.duration= 0
        self.verbose= print

    # Game interface :
    def initialize(self):
        # Initialize a new game (returning the game setting as a Gamel, a game ellement shared with player wake-up)
        f= open(f"{gamePath}/ressources/map-{self.map}.gml")
        self.board=  hg.Board().load( f.read() )
        f.close()
        for i in range(1, self.numberOfPlayers+1) :
            self.appendArmy( i, i, 12, 1 )
            #self.board.cell( i ).append-Child( hg.Gamel( "Army", self.playerLetter(i), [1, 12] ) )
        self.counter= 1
        if self.duration == 0 :
            self.duration= self.board.numberOfCells()
        self.board.setAttributes( [ self.counter, self.duration ] )
        return self.board
        
    def playerHand( self, iPlayer ):
        # Return the game elements in the player vision (an AbsGamel)
        self.board.setStatus( self.playerLetter(iPlayer) )
        self.board.setAttributes( [ self.counter, self.duration ] )
        return self.board

    def applyPlayerAction( self, iPlayer, action ):
        # Apply the action choosen by the player iPlayer. return a boolean at True if the player terminate its actions for the current turn.
        action= action.split(' ')
        if action[0] == "move" and len( action ) == 4 :
            return self.actionMove( iPlayer, int(action[1]), int(action[2]), int(action[3]) )
        if action[0] == "grow" :
            return self.actionGrow( iPlayer, int(action[1]) )
        if action[0] == "sleep" :
            return self.actionSleep( iPlayer )
        print( "!!! Wrong action: {action} !!!" )
        return False

    def actionMove( self, iPlayer, iFrom, iTo, force ):
        target= self.board.cell(iTo)
        if len( self.board.cell(iFrom).children() ) > 0 :
            army= self.board.cell(iFrom).child()
            actCounter= army.attribute(ACTION)
            playerLetter= self.playerLetter(iPlayer)
            if playerLetter == army.status() and actCounter > 0 :
                # All the army ?
                if force >= army.attribute(FORCE) :
                    force= army.attribute(FORCE)
                    self.board.cell(iFrom).popChild(1)
                else :
                    army.decreaseAttribute(FORCE, force)
                # free target:
                if len( target.children() ) == 0 :
                    self.appendArmy( iPlayer, iTo, force, action= actCounter-1 )
                # friend target:
                elif target.child().status() == playerLetter :
                    targetArmy= target.child()
                    targetArmy.increaseAttribute(FORCE, force)
                    targetArmy.setAttribute( ACTION, min( targetArmy.attribute(ACTION), actCounter-1) )
                else: 
                    self.actionFight( iPlayer, actCounter, force, iTo )
            else :
                print( f"!!! Wrong move: unvalid army on {iFrom}!!!" )
        else :
            print( f"!!! Wrong move: no army on {iFrom} !!!" )
        return False
        
    def actionFight( self, iPlayer, actCounter, attack, iTo ):
        # Initialize:
        defence= self.board.cell(iTo).child().attribute(FORCE)
        # while fighters:
        while attack > 0 and defence > 0 :
            degatAtt, degatDef= self.degatMethod(attack, defence)
            self.verbose( f"Fight-{iTo}: {attack}({degatAtt}) vs {defence}({degatDef})" )
            attack= max( 0, attack - degatDef )
            defence= max( 0, defence - degatAtt )
        # Update cell: defence
        self.verbose( f"Fight-{iTo}: {attack} vs {defence}" )
        if defence == 0 :
            self.board.cell(iTo).popChild()
        else :
            self.board.cell(iTo).child().setAttribute(FORCE, defence)
        # Update cell: attack
        if attack > 0 :
            self.appendArmy( iPlayer, iTo, attack, action= actCounter-1 )
            self.appendArmy( iPlayer, iTo, attack )

    def degatDeterministic( self, attack, defence ):
        attackForce= attack + max(0, attack - defence)
        return (1+attackForce)//2, (2+defence*2)//3

    def degatStochastic( self, attack, defence ):
        attackForce= attack + max(0, attack-defence)
        degatAtt= 1
        for i in range( attackForce ):
            if random.randrange(12) < 5 :
                degatAtt+= 1
        degatDeff= 0
        for i in range( defence ):
            if random.randrange(12) < 8 :
                degatDeff+= 1
        return degatAtt, degatDeff

    def actionSleep( self, iPlayer ):
        playerLetter= self.playerLetter(iPlayer) 
        for cell in self.board.cells() :
            for army in cell.children() :
                if army.status() == playerLetter :
                    army.setAttribute( ACTION, min( 2, army.attribute(ACTION)+1) )
        return True

    def actionGrow( self, iPlayer, iCell ):
        playerLetter= self.playerLetter(iPlayer)
        army= self.board.cell( iCell ).child()
        recrut= (2+army.attribute(FORCE))//3
        if army and army.status() == playerLetter and army.attribute(ACTION) > 0 :
            for iNeighbour in self.board.edges( iCell) :
                if self.board.cell( iNeighbour ).child() and self.board.cell( iNeighbour ).child().status() == playerLetter :
                    recrut+= 1
            if self.board.cell( iCell ).child().attribute(FORCE) > 0 :
                self.board.cell( iCell ).child().increaseAttribute(FORCE, recrut)
            army.decreaseAttribute(ACTION, 1)
        return False

    def tic( self ):
        # called function at turn end, after all player played its actions. 
        self.counter= min( self.counter+1, self.duration )

    def isEnded( self ):
        # must return True when the game end, and False the rest of the time.
        return len( self.activePlayers() ) == 1 or self.counter >= self.duration

    def activePlayers(self):
        active= []
        for cell in self.board.cells() :
            for army in cell.children() :
                iPlayer= self.playerNum( army.status() )
                if iPlayer not in active :
                    active.append( iPlayer )
                    active.sort()
        return active
    
    def playerArmies(self):
        armies= [ 0 for i in range( self.numberOfPlayers+1 ) ]
        for cell in self.board.cells() :
            for army in cell.children() :
                iPlayer= self.playerNum( army.status() )
                armies[ iPlayer ]+= army.attribute(FORCE)
        return armies
    
    def playerScore( self, iPlayer ):
        # return the player score for the current game (usefull at game ending)
        armies= self.playerArmies()
        bestArmy= armies[0]
        winners= 0
        for i in range(1, self.numberOfPlayers+1) :
            if armies[i] > bestArmy :
                bestArmy= armies[i]
                winners= 1
            elif armies[i] == bestArmy :
                winners+= 1
        if winners == 1 and armies[iPlayer] == bestArmy :
            return 1
        return armies[iPlayer] - bestArmy
    
    # Risky tools :
    def appendArmy( self, iPLayer, position, force, action= 0 ):
        army= hg.Gamel( "Army", self.playerLetter(iPLayer), [action, force] )
        self.board.cell(position).appendChild( army )

    def playerLetter(self, iPlayer):
        return chr( ord("A")+iPlayer-1 )

    def playerNum(self, playerLetter):
        return 1 + ord(playerLetter) - ord("A")
