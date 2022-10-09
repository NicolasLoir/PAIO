#!env python3
"""
S: set of states
A: set of actions
P: transition function
R: reward function
"""

A = []
for a1 in ['keep', 'roll']:
    for a2 in ['keep', 'roll']:
        for a3 in ['keep', 'roll']:
            A.append( a1+'-'+a2+'-'+a3 )
S = []
for h in range( 3 ) :
    for i1 in range(1, 7) :
        for i2 in range(1, i1+1) :
            for i3 in range(1, i2+1) :
                # state= { "H":h,  D1:i1,  D2:i2,  D3:i3 }
                state = f"{h}[{i1},{i2},{i3}]"
                S.append( state )

def main():
    print(A)
    print(S)
    print(len(S))
    V, optimal_policy = value_iterations(S, A, P, R)
    # print("\n---------------\n")
    # print(V)
    # print(optimal_policy)
    total = 0
    score = 0
    for v in V:
        total += 1
        score += V[v]
    print(score/total)

def H(state):
    return state[0]

def D1(state):
    return state[2]

def D2(state):
    return state[4]

def D3(state):
    return state[6]

def value_iterations(S, A, P, R):
    V = {s: 0 for s in S}
    optimal_policy = {s: 0 for s in S}
    i = 0
    while i < 100:
        oldV = V.copy()
        print(i)
        for s in S:
            Q = {}
            for a in A:
                somme = 0
                for s_next in S:
                    # print(f'P(s_next, s, a): {P(s_next, s, a)}')
                    # print(f'oldV[s_next]: {oldV[s_next]}')
                    somme += P(s_next, s, a) * oldV[s_next]
                # print(f'somme: {somme}')
                # print(f'R(s,a): {R(s,a)}')
                Q[a] = R(s,a) + somme
                # print(f'Q[a]: {Q[a]}')
                # Q[a] = R(s,a) + sum( (P(s_next, s, a) * oldV[s_next]) for s_next in S)
            V[s] = max(Q.values())
            optimal_policy[s] = max(Q, key=Q.get)
        if (all(oldV[s] == V[s] for s in S)):
            print("break")
            break
        i+=1
        print(V)
        print(optimal_policy)
        print("\n---------------\n")
    return V, optimal_policy

def R(s, a):
    if int(H(s)) == 0:
        return score(s)
    else:
        return 0

def score(state):
    if int(D1(state)) == 4 and int(D2(state)) == 2 and int(D3(state)) == 1 : 
        return 800
    if int(D1(state)) == 1 and int(D2(state)) == 1 and int(D3(state)) == 1 : 
        return 600
    if int(D2(state)) == 1 and int(D3(state)) == 1 : 
        return 400 + int(D1(state))
    if int(D2(state)) == int(D1(state)) and int(D3(state)) == int(D1(state)) : 
        return 300 + int(D1(state))
    if int(D2(state)) == int(D1(state))-1 and int(D3(state)) == int(D1(state))-2 : 
        return 200 + int(D1(state))
    if int(D1(state)) == 2 and int(D2(state)) == 2 and int(D3(state)) == 1 : 
        return 0
    return 100 + int(D1(state))

def P(s_next, s, a):
    # print(f's_next: {s_next}')
    # print(f's: {s}')
    # print(f'a: {a}')
    if H(s_next) == str(int(H(s)) - 1):
        # print("ici")
        if a == "keep-keep-keep" and D1(s_next) == D1(s) and D2(s_next) == D2(s) and D3(s_next) == D3(s):
            return 1
        elif a == "roll-keep-keep" and oneRoll(s_next, s, D2, D3):
            return 1/21
        elif a == "keep-roll-keep" and oneRoll(s_next, s, D1, D3):
            return 1/21
        elif a == "keep-keep-roll" and oneRoll(s_next, s, D1, D2):
            return 1/21
        elif a == "keep-roll-roll" and D1(s_next) == D1(s):
            if int(D1(s)) == 1:
                return 1
            elif int(D1(s)) == 2:
                return 1/3
            elif int(D1(s)) == 3:
                return 1/6
            elif int(D1(s)) == 4:
                return 1/10
            elif int(D1(s)) == 5:
                return 1/15
            elif int(D1(s)) == 6:
                return 1/21
        elif a == "roll-keep-roll" and D2(s_next) == D2(s):
            if int(D2(s)) == 1:
                return 1/6
            elif int(D2(s)) == 2:
                return 1/10
            elif int(D2(s)) == 3:
                return 1/12
            elif int(D2(s)) == 4:
                return 1/12
            elif int(D2(s)) == 5:
                return 1/10
            elif int(D2(s)) == 6:
                return 1/6
        elif a == "roll-roll-keep" and D3(s_next) == D3(s):
            if int(D3(s)) == 1:
                return 1/21
            elif int(D3(s)) == 2:
                return 1/15
            elif int(D3(s)) == 3:
                return 1/10
            elif int(D3(s)) == 4:
                return 1/6
            elif int(D3(s)) == 5:
                return 1/3
            elif int(D3(s)) == 6:
                return 1
        elif a == "roll-roll-roll":
            return 1/56
        else:
            return 0
    else:
        return 0

#dice are sorted
def oneRoll(s_next, s, dA, dB):
    return (D2(s_next) == dA(s) and D3(s_next) == dB(s)) \
            or (D1(s_next) == dA(s) and D2(s_next) == dB(s)) \
            or (D1(s_next) == dA(s) and D3(s_next) == dB(s))

# script
if __name__ == '__main__' :
    main()