# 421, an HackaGames game (hum)

**421** is simple dice games where one unique player try to optimize it dice combination after a maximum of 2 roll dice steps.

## Installation

**421** (as **HackaGames**) is natively developed on and for Linux systems.
Commands are given regarding Ubuntu-like distribution.

**421** is included in the minimal **HackaGames** package (i.e. nothing to do here).

## Try the game:

**421** is a standard **HackaGames** game, and it works with a client-server architecture.
The server is the game, the clients are the players.
**421** can be played in a _solo_ or a _2-players_ mode. 

First start the game server (from **HackaGames** repository) in default _solo_ mode :

```sh
./game-421/start
```

Then, in a new terminal start the basic **HackaGames** terminal player:

```sh
./play.py
```

The player can perform one and only one action at it turns, and the game stops automatically after 2 turns.

The actions consist in keeping or rolling each of the 3 dices. So there are 8 actions:

- `keep-keep-keep`,  `keep-keep-roll`,  `keep-roll-keep`,  `keep-roll-roll`, `roll-keep-keep`,  `roll-keep-roll`,  `roll-roll-keep` and `roll-roll-roll`

The goal is to optimize the combination of dices before the end of the 2 turns.
The best combination ever is **421**.
But you can explore other combinations.

_Optionnally_, the script "`local`" permit annyone to launch the game without the _client_-_server_ protocol.



## Let an AI play:

The file `./game-421/firstAI.py` propose a first random AI with the required structure to play **421**.

to test the player start the server and this player in 2 differents terminals:

```sh
./game-421/start
```

then:

```sh
./game-421/firstAI.py
```

To notice that, you can incresse the numbers of games with the `-n` attribute:

```sh
#terminal 1:
./game-421/start -n 1000
#terminal 2:
./game-421/firstAI.py
```

## Your first AI:

In a directory dedicated to your work, you start an AI from the proposed random player:

```bash
mkdir myPlayers
cp game-421/firstAI.py myPlayers/my421IA.py
```

An **HackaGames** player is composed by 4 main methods: `wakeUp`, `perceive`, `decide` and `sleep`

In python: 

```python
    # Player interface :
    def wakeUp(self, playerId, numberOfPlayers, gameConfigurationMsg):
        self.scores= [ 0 for i in range(numberOfPlayers+1) ]
        self.id= playerId
        print( '> ' + '\n'. join([ str(line) for line in gameConfigurationMsg ]) )

    def perceive(self, gameStatusMsg):
        gameStatus= gameStatusMsg[0].split(' ')
        self.horizon= int(gameStatus[1])
        self.dices= [ int(gameStatus[3]), int(gameStatus[4]), int(gameStatus[5]) ]
        print( '> ' + '\n'. join([ str(line) for line in gameStatusMsg ]) )
        print( f'H: {self.horizon} DICES: {self.dices}' )

    def decide(self):
        action= random.choice( actions )
        return action
    
    def sleep(self, result):
      print( f'--- Results: {str(result)}' )
```



## Play Battle:
