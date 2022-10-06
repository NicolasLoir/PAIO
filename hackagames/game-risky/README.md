# Risky, an HackaGames Game

Risky is a strategic turn-based game where two army fights for a territory.

Board exemple (board-4, empty): 

```
       .' '.
      |     |
       '. .'3
      /     \
 .' '.       .' '.
|     |-----|     |
 '. .'1      '. .'2 
      \     /
       .' '.
      |     |
       '. .'4
```

A player node : 

```
 .'A'.    # Player ID
|1-100|   # army action and force 
 '. .'1   # node ID
```



move A B 100




## Installation

**Risky** is part of **HackaGames** project. Please refer to the **HackaGames** installation procedure.

## Try the game:

A **HackaGames** game works as a server and the players have to connect (seat on a game) to play the games.
So players are independent processes working as clients.

### Start the game

First start `risky` server in a first terminal: 

```sh
./hg-risky
```

Then 2 players have to reach the games on port 14001, so in two different terminals:

For a human player:

```sh
telnet localhost 14001
```

For AI player (in python in the example):

```sh
python3 simplePlayer.py
```

Then the second terminal (telnet) is waiting for an action of your choice.
Each player can perform one and only one action at it turns.

- moving: `move X Y STRENGH` to move `STRENGH` units from cell `X` to cell `Y`
- growing: `grow X` to grow the army on nodes `X`
- sleeping: `sleep` that reset the action counter to $0$ for all the armies (each army need to sleep between 2 move or grow actions).

### Game rules

At the beginning of the game, each player receives a description of the tabletop, the cells and the edges connection.
The edges model the possible movements.

At its turn, each player gets a state of the game:
- player: the player configuration (its player id (1 or 2) the number of players (2) the current scores for player-1 and player-2 )
- Game: the number of turns before the end of the game and the number of pieces (i.e. armies) on the tabletop.
- Pieces: the list of pieces on the tabletop. The position cell, the player owner, a type (always soldier here) a list of 2 attributes (strength and number of performed actions).
After what the game would expect a decision.

Each player can perform one and only one action at it turns.

- moving: `move X Y STRENGH` to move `STRENGH` units from nodes `X` to node `Y`
- growing: `grow X` to grow the army on nodes `X`
- sleeping: `sleep` that reset the action counter to $0$ for all the miniatures.

To notice that:

- A piece can perform only one action between to sleep.
- A wrong action request would end on a sleep action.
- A moving action on an occupied cell would merge or fight the targeted cell depending on the owner.
- A fight is always to the death of one of the two pieces. 


## Your first AI:

The file `simplePlayer.py` propose a first random AI with the required structure to play `risky`.
So copy this player and start to implement simple ideas...

```bash
cp simplePlayer.py myBeatifullAI.py
```

first terminal: 

```sh
./hg-risky
```

Second terminal:

```sh
python3 simplePlayer.py
```

Third terminal:

```sh
python3 myBeatifullAI.py
```

## Game-Risky parameters:

Risky game server can be launched with `hg-risky` or `hg-risky-hidden` for ecconomize the viewer.
Those two command take few arguments: 

- **Argument-1**: The number of games the tow player would play (default 1). It usefull to test make statistics. At each new games the first ans second player switch.
- **Argument-2**: The number of turn (default 30). The games will end after *Argument-2* turns.
- **Argument-3**: Server port.

For instance, `hg-risky-hidden 1000 24` would launchs 1000 games of 24 turns between the two player-clients connecting the server.

# Next version: 

Increase the importance of action points:

Army would have a max of 3 action points.

**Sleep Node**: return 2 action points.
**Move Node  Node Force**: cost 1 action points.
**Move+Attack**: cost 2 action points (other wise the reminder attanquant would be distroy)
**Defending**: cost 1 action-points (if action points are availlable)
**Grow Node**: cost 2 action points

A new actions would be availlable: 

**overstate Node**: sacrify the army on node `Node` to regaint 2 action-points. 1/7 of the army is distroy in the process.
