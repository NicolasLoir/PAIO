#!env python3
import socket, hackapy
from . import element, interprocess, game, player, cmd

# HackaGames Elements
AbsGamel= element.AbsGamel
Gamel= element.Gamel
Board= element.Board
AbsPlayer= player.AbsPlayer
AbsGame= game.AbsGame
AbsSequentialGame= game.AbsSequentialGame
AbsSimultaneousGame= game.AbsSimultaneousGame

#Piece= game.Piece
#Cell= game.Cell
#Tabletop= game.Tabletop

# Command tools
StartCmd= cmd.StartCmd
