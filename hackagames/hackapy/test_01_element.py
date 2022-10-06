# HackaGames UnitTest - `pytest`

from . import element as elt

Gamel= elt.Gamel

# ------------------------------------------------------------------------ #
#                   T E S T   H A C K A G A M E S - E L E M E N T
# ------------------------------------------------------------------------ #

def test_Gamel_init():
    gamel= Gamel()
    assert gamel.type() == "elt"
    assert gamel.status() == ""
    assert gamel.attributes() == []
    assert gamel.values() == []
    assert gamel.cells() == []

def test_Gamel_dump():
    gamel= elt.Gamel()
    assert gamel.dump() == "elt 0 0 0 0 :" # set: "elt-00 (0 0 0 0) state: attrs: values: cells:"
    gamel.setAttributes([3, 8])
    assert gamel.dump() == "elt 0 2 0 0 : 3 8"
    gamel.append( elt.Gamel( 'elt', 'bob happy', [4], [0.6, 10.0] ) )
    assert gamel.dump() == "elt 0 2 0 1 : 3 8\n- elt 2 1 2 0 : bob happy 4 0.6 10.0"
    gamel.append( elt.Gamel() )
    assert '\n'+ gamel.dump() +'\n' == """
elt 0 2 0 2 : 3 8
- elt 2 1 2 0 : bob happy 4 0.6 10.0
- elt 0 0 0 0 :
"""

def test_Gamel_load():
    gamel= Gamel( 'board', 'SouriCity', [3, 8] )
    gamel2= Gamel().load( gamel.dump() )
    assert '\n'+ gamel2.dump()  +'\n' == """
board 1 2 0 0 : SouriCity 3 8
"""
    gamel.append( Gamel( 'human', 'bob happy', [4] ) )
    gamel.append( Gamel( 'human', 'lucy' ) )
    gamel3= Gamel().load( gamel.dump() )
    assert '\n'+ gamel3.dump()  +'\n' == """
board 1 2 0 2 : SouriCity 3 8
- human 2 1 0 0 : bob happy 4
- human 1 0 0 0 : lucy
"""

def test_Gamel_deepDump():
    gamel= Gamel( 'board', 'SouriCity', [3, 8] )
    bob= Gamel( 'human', 'bob', [4] )
    bob.append( Gamel('action', 'Attack', [10]) )
    bob.append( Gamel('action', 'Move', [], [2.0]) )
    gamel.append( bob )
    gamel.append( Gamel( 'human', 'lucy happy' ) )
    assert '\n'+ gamel.dump()  +'\n' == """
board 1 2 0 2 : SouriCity 3 8
- human 1 1 0 2 : bob 4
  - action 1 1 0 0 : Attack 10
  - action 1 0 1 0 : Move 2.0
- human 2 0 0 0 : lucy happy
"""

def test_Gamel_deepLoad():
    gamel= Gamel( 'board', 'SouriCity', [3, 8] )
    bob= Gamel( 'human', 'bob', [4] )
    bob.append( Gamel('action', 'Attack', [10]) )
    bob.append( Gamel('action', 'Move', [], [2.0]) )
    gamel.append( bob )
    gamel.append( Gamel( 'human', 'lucy happy' ) )
    gamel2= Gamel().load( gamel.dump() )
    assert '\n'+ gamel2.dump()  +'\n' == """
board 1 2 0 2 : SouriCity 3 8
- human 1 1 0 2 : bob 4
  - action 1 1 0 0 : Attack 10
  - action 1 0 1 0 : Move 2.0
- human 2 0 0 0 : lucy happy
"""
