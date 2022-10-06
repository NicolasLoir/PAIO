#!env python3

from qlearning import Qlearning421 as iaQlearning421

def main():
    iaQlearning = iaQlearning421()
    iaQlearning.train(10000000)
    print("ok")

if __name__ == '__main__' :
    main()