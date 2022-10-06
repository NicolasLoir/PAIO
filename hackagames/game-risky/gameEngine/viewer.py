#!env python3
"""
HackaGame risky interface 
"""

import sys, os

sys.path.insert(1, os.path.join(sys.path[0], '..'))

import hackapy as hg

gamePath= os.path.join(sys.path[0])

class ViewerTerminal:

    # Player interface :
    def __init__( self, aBoard ):
        self.board= aBoard
        self.generateGrid()
        mapFile= f"{gamePath}/ressources/map-{self.board.status()}.txt"
        if os.path.exists( mapFile ) :
            self.loadGridBackground( mapFile )

    # grid: 
    def generateGrid(self):
        maxLine= 4
        maxLenght= 1
        for i in range( self.board.numberOfCells() ) :
            if self.board.cell(i).attribute(1) > maxLine :
                maxLine= self.board.cell(i).attribute(1)
            if self.board.cell(i).attribute(2) > maxLenght :
                maxLenght= self.board.cell(i).attribute(2)
            
        print( f"Grid size: ({maxLine}, {maxLenght})" )
        self.grid= [ [' ' for i in range(maxLenght+4) ] for line in range(maxLine+2) ]

    def loadGridBackground( self, mapFile ):
        f= open(mapFile)
        iLine= 0
        for line in f.readlines() :
            for iCol in range( len(line)-1 ) :
                self.grid[iLine][iCol]= line[iCol]
            iLine+= 1
    
    # Print: 
    def print(self):
        print( f'---\ngame state: player-{ self.board.status() } (turn { self.board.attribute(1) } over { self.board.attribute(2) })' )
        grid= [ [ x for x in line ] for line in self.grid ]
        for cell in self.board.cells() :
            cellId= str(cell.type().split('-')[1])
            line, col = cell.attribute(1), cell.attribute(2)
            if len( cell.children() ) > 0 :
                self.printArmyOnGrid( cell.child(1), grid, line, col )
            
            l= len(cellId)
            for i in range(l) :
                grid[line+1][col+3-l+i]=  cellId[i]

        for line in grid :
            print( '| '+ ''.join( line ) + ' |' )

    def printArmyOnGrid(self, army, grid, line, col):
        grid[line-1][col]= army.status()
        grid[line][col-2]= str(army.attribute(1))
        grid[line][col-1]= '-'
        force= str(army.attribute(2))
        while len( force ) < 3 :
            force= ' '+force
        grid[line][col]= force[0]
        grid[line][col+1]= force[1]
        grid[line][col+2]= force[2]
                
                