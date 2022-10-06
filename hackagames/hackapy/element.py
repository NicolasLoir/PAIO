
from sre_parse import State


def main() :
    # Debuging tests...
    print("Cool")

class AbsGamel():
    
    # Abs Accessor :
    def status(self):
        pass

    def attributes(self):
        # must return a list of integers
        pass

    def values(self):
        # must return a list of floating point numbera
        pass

    def children(self):
        # must return a list of AbsGamel objects
        pass
    
    # Abs Modifiers :
    def setAttributes(self, aListOfIntergers):
        pass
        
    def setValues(self, aListOfFloats):
        pass
    
    def resetChildren(self):
        pass
        
    def setStatus(self, aStr):
        self._status= aStr

    def loadChild( self, childBuffer ):
        pass
    
    # Modifiers :
    def dump(self, ident= 0):
        newLine= '\n'
        for i in range(ident) :
            newLine+= '  '
        newLine+= '- '
        status= self.status()
        attrs= self.attributes()
        values= self.values()
        children= self.children()
        statusSize= 0
        if status != '' :
            statusSize= status.count(' ')+1
        attrsSize= len( attrs )
        valuesSize= len( values )
        childrenSize= len( children )
        msg= f'{self.type()} {statusSize} {attrsSize} {valuesSize} {childrenSize} :'
        if statusSize > 0 :
            msg += ' '+ status
        if attrsSize > 0 :
            msg+= ' '+ ' '.join( str(i) for i in attrs )
        if valuesSize > 0 :
            msg+= ' '+ ' '.join( str(i) for i in values )
        for c in children :
            msg+= newLine + c.dump(ident+1)
        return msg
    
    def load(self, buffer):
        if type(buffer) == str :
            buffer= buffer.split('\n')
        line= buffer.pop(0)
        # Get meta data (type, name and structure sizes):
        metas, params= tuple( line.split(' :') )
        metas= metas.split(' ')
        self.setType( metas.pop(0) )
        metas= [ int(x) for x in metas ]
        statusSize, attrsSize, valuesSize, childrenSize= tuple( metas )
        if statusSize + attrsSize + valuesSize > 0 :
            params= params[1:].split(' ')
            status= ''+ ' '.join( [ params.pop(0) for i in range(statusSize) ] )
            self.setStatus( status )
            attrs= [ int(params.pop(0)) for i in range(attrsSize) ]
            self.setAttributes( attrs )
            values= [ float(params.pop(0)) for i in range(valuesSize) ]
            self.setValues( values )
        # load children
        self.resetChildren()
        if childrenSize > 0 :
            iChild= 0
            while buffer and buffer[0][0:2] == '- ' :
                childBuffer= [ buffer.pop(0)[2:] ]
                while buffer and buffer[0][0:2] == '  ' :
                   childBuffer.append( buffer.pop(0)[2:] )
                self.loadChild( childBuffer )
        return self

    def __str__(self):
        return self.str(0)
    
    def str(self, ident):
        newLine= '\n'
        for i in range(ident) :
            newLine+= '  '
        newLine+= '- '
        status= self.status()
        attrs= self.attributes()
        values= self.values()
        children= self.children()
        statusSize= 0
        if status != '' :
            statusSize= status.count(' ')+1
        attrsSize= len( attrs )
        valuesSize= len( values )
        msg= f'{self.type()} :'
        if statusSize > 0 :
            msg += ' '+ status
        if attrsSize > 0 :
            msg+= ' ['+ ', '.join( str(i) for i in attrs ) + "]"
        if valuesSize > 0 :
            msg+= ' ('+ ', '.join( str(i) for i in values ) + "]"
        for c in children :
            msg+= newLine + c.str(ident+1)
        return msg

class Gamel(AbsGamel):

    def __init__( self, eltType="elt", status= "", attributes=[], values=[] ):
        self._type= eltType
        self._status= status
        self._attrs= attributes
        if not bool(attributes) :
            self._attrs= []
        self._values= values
        if not bool(values) :
            self._values= []
        self._children= []

    # Gamel Accessors:
    def type(self):
        return self._type

    def status(self):
        return self._status

    def attributes(self):
        return self._attrs
        
    def values(self):
        return self._values
    
    def children(self):
        return self._children
    
    def attribute(self, i):
        assert( 1 > 0 )
        return self._attrs[i-1]
        
    def child(self, i=1):
        if len( self._children ) == 0 :
            return False
        assert( 1 > 0 )
        return self._children[i-1]
        
    def value(self, i):
        assert( 1 > 0 )
        return self._values[i-1]

    # Gamel Modification:
    def setFrom(self, aGamel):
        self._type= aGamel.type()
        self._status= aGamel.status()
        self._attrs= aGamel.attributes()
        self._values= aGamel.values()
        self._children= aGamel.children()
        return self

    def setType(self, aStr):
        self._type= aStr
    
    def setStatus(self, aStr):
        self._status= aStr
    
    def setAttributes(self, aListOfIntergers):
        self._attrs= aListOfIntergers
    
    def setAttribute(self, i, anInteger):
        self._attrs[i-1]= anInteger
    
    def increaseAttribute(self, i, anInteger):
        self._attrs[i-1]+= anInteger
    
    def decreaseAttribute(self, i, anInteger):
        self._attrs[i-1]-= anInteger
    
    def setValues(self, aListOfFloats):
        self._values= aListOfFloats

    def increaseValue(self, i, anFloat):
        self._values[i-1]+= anFloat
    
    def decreaseValue(self, i, anFloat):
        self._values[i-1]-= anFloat

    def resetChildren(self):
        self._children= []
    
    def appendChild(self, child):
        self._children.append(child)
        return self
    
    def popChild(self, i=1):
        self._children.pop(i-1)

    def loadChild( self, childBuffer ):
        child= Gamel()
        self._children.append( child.load(childBuffer) )
        return child
    
class Board(Gamel):

    def __init__( self, numberOfCells= 0 ):
        super().__init__("Board")
        for i in range(numberOfCells) :
            self._children.append( Gamel( f"Cell-{i+1}" ) )
            self._children.append( Gamel( f"Edge-{i+1}" ) )

    def numberOfCells(self):
        return len(self._children)//2

    def cell(self, iCell):
        return self._children[ (iCell-1)*2 ]

    def cells(self):
        return ItCells( self )

    def edges(self, iCell):
        return self._children[ (iCell-1)*2 + 1 ].attributes()

    def isEdge(self, iFrom, iTo):
        return iTo in self.edgeFrom(iFrom)._attrs

    def connect(self, iFrom, iTo):
        fromEdge= self.edgeFrom(iFrom)
        if iTo not in fromEdge._attrs :
            fromEdge._attrs.append(iTo)
            fromEdge._attrs.sort()
        return self

class ItCells:
    """Iterator over board cells"""
    def __init__(self, board):
        self.board= board
        self.i= 1

    def __iter__(self):
        self.i = 1
        return self

    def __next__(self):
        if self.i <= self.board.numberOfCells() :
            result = self.board.cell( self.i )
            self.i += 1
            return result
        else:
            raise StopIteration

# script
if __name__ == '__main__' :
    main()