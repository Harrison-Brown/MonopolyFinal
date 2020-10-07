# Function to verify that columns are probability vectors
def checkcol(P):
    for i in [sum(x) for x in P.T]:
        if i != 1:
            return False
    return True

# Create blank matrix to fill in
# Matrix notation P[row, col], or P[to, from]
P = matrix(QQ, 44, 44)

# Create tiles for identification
Tiles = ['Go', 'Mediterranean Ave', 'Community Chest', 'Baltic Ave', 'Income Tax', 'Reading Railroad', 'Oriental Ave', 'Chance', 'Vermont Ave', 'Connecticut Ave', 'Pass Jail',
         'St. Charles Place', 'Electric Company', 'States Ave', 'Virvinia Ave', 'Pennsylvania Railroad', 'St. James Place', 'Community Chest', 'Tennessee Ave', 'New York Ave', 'Free Parking',
         'Kentucky Ave', 'Chance', 'Indiana Ave', 'Illinois Ave', 'B & O Railroad', 'Atlantic Ave', 'Ventnor Ave', 'Water Works', 'Marvin Gardens', 'Go To Jail',
         'Pacific Ave', 'North Carolina Ave', 'Community Chest', 'Pennsylvania Ave', 'Short Line', 'Chance', 'Park Place', 'Luxury Tax', 'Boardwalk', 'Jail', 'Jail1', 'Jail2', 'Jail3']

# Define all possible dice rolls
RollProbability = [1/36, 2/36, 3/36, 4/36, 5/36, 6/36, 5/36, 4/36, 3/36, 2/36, 1/36]
    # Possible dice rolls:
    #    2,    3,    4,    5,    6,    7,    8,    9,   10,   11,   12
    # 1/36, 2/36, 3/36, 4/36, 5/36, 6/36, 5/36, 4/36, 3/36, 2/36, 1/36

# Create probabilities for rolling dice
for i in range(28):
    P[i+2:i+13, i] = vector(RollProbability)

    
# Account for loop around
for i in range(27, 39):
    P[i+2:40, i] = vector(RollProbability)[:38-i]
    P[:i-27, i] = vector(RollProbability)[38-i:]

# Account for state 39 (didn't slice)
P[1:12, 39] = vector(RollProbability)

# Account for staying in jail
# Jail is state 40 --> 43
# Passing jail is state 11
for i in range(40, 43):
    P[i+1, i] = 30/36 # likelhood of going to next jail
    P[11, i] = 6/36 # likelihood of leaving jail (roll doubles)
# 3 attempts then forced to leave jail
P[11, 43] = 1

# Account for chance cards
# Chance states are 8, 22, 36
for i in range(40):
    # Find probabilities of getting to chance
    chance1 = P[8, i]
    chance2 = P[22, i]
    chance3 = P[36, i]

    # Chance of staying on chance tile
    # 9 options to move, 7 option to stay
    # 11/20 chance to stay (or move)
    P[8, i] = chance1 * (7/16)
    P[22, i] = chance2 * (7/16)
    P[36, i] = chance3 * (7/16)

    # Add probability of chance card to existing states
    # Ex. prob of getting to go is the current dice roll
    # plus prob of landing on any chance * 1/20 (20 unique card states)

    # First nested loop for Go, Illinois, St. Charles, Jail, Boardwalk, and Reading Railroad
    for j in [0, 24, 11, 40, 39, 5]:
        P[j, i] = P[j, i] + (chance1 + chance2 + chance3)*(1/16)

    # Head to nearest utility
    # Varies with where chance is
    # Landing on electric varies only with chance 1 and 3
    P[12, i] = P[12, i] + (chance1 + chance3)*(1/16)
    # Landing on water only varies with chance 2
    P[28, i] = P[28, i] + (chance2)*(1/16)

    # Head to nearest railroad
    # Same as utilities
    P[5, i] = P[5, i] + (chance3)*(1/16)
    P[15, i] = P[15, i] + (chance1)*(1/16)
    P[25, i] = P[25, i] + (chance2)*(1/16)
    # Railroad at 35 cannot be advanced to from chance

    # Back 3 spaces
    P[(i-3)%40, i] = P[(i-3)%40, i] + (chance1 + chance2 + chance3)*(1/16)

# Account for community chest cards
# Community chests only go to Go and Jail
for i in range(40):
    # Find probabilities of getting to community chest
    chest1 = P[2, i]
    chest2 = P[17, i]
    chest3 = P[33, i]

    # Probability of no movement
    P[2, i] = chest1 * (15/17)
    P[17, i] = chest2 * (15/17)
    P[33, i] = chest3 * (15/17)

    # Advance to go
    P[0, i] = P[0, i] + (chest1 + chest2 + chest3)*(1/17)

    # Go to jail
    P[40, i] = P[40, i] + (chest1 + chest2 + chest3)*(1/17)

# Check if columns are probability vectors
#if checkcol(P):
#    print "all good"
#else:
#    print "not good"
#    print [sum(x) for x in P.T]


# Set up player vector
# All players start at Go
player = matrix(QQ, 44, 1)
player[0, 0] = 1

# Find steady-state vector
S = P**1001 * player

# Turn S into decimal approximation to avoid large fractions
S_a = N(S, digits = 4)

Rent = [0,2,0,4,0,25,6,0,6,8,0,10,28,10,12,25,14,0,14,16,0,18,0,18,20,25,22,22,28,24,0,26,26,0,28,25,0,35,0,50, 0, 0, 0, 0]
print '   Tile                   Probability   Revenue'
for i in range(44):
    print "{:2} {:22} {:8}      ${:3}".format(i, Tiles[i], S_a[i, 0], S_a[i, 0]*Rent[i] )

# Find order of probabilities for questions
order = S_a.list()
for i in range(44, 0, -1):
    order[order.index(min(order))] = i

print '\nTop 10 tiles - Probability'
for i in range(1, 11):
    print "Tile {:2}, {:.4}%".format(order.index(i), S_a[order.index(i), 0] * 100)

print '\nTop 10 expected values - single property'

S_a = S_a.list()

ExpectedRent = [Rent[i]*S_a[i] for i in range(40)]
for i in range(10):
    x = ExpectedRent.index(max(ExpectedRent))
    y = ExpectedRent.pop(x)
    print 'Tile {:2}, ${:.4}'.format(x, y)

Brown = 4*S_a[1] + 8*S_a[3]
Cyan = 12*S_a[6] + 12*S_a[8] + 16*S_a[9]
Pink = 20*S_a[11] + 20*S_a[13] + 24*S_a[14]
Orange = 28*S_a[16] + 28*S_a[18] + 32*S_a[19]
Red = 36*S_a[21] + 36*S_a[23] + 40*S_a[24]
Yellow = 44*S_a[26] + 44*S_a[27] + 48*S_a[28]
Green = 52*S_a[31] + 52*S_a[32] + 52*S_a[34]
Blue = 70*S_a[37] + 100*S_a[36]
Util = 70*S_a[12] + 70*S_a[28]
RR = 200*S_a[5] + 200*S_a[15] + 200*S_a[25] + 200*S_a[35]

print '\nExpected revenue from each set of properties'
Property = {'Brown':Brown,'Cyan':Cyan,'Pink':Pink,'Orange':Orange,'Red':Red,'Yellow':Yellow,'Green':Green,'Blue':Blue,'Util':Util,'RR':RR}
for i in Property:
    print '{}, ${:.2f}'.format(i, float(Property[i]))
