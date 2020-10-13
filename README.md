# MonopolyFinal
SageMath script to find expected revenues of properties in Monopoly. Runs in CoCalc/SageMath environment.

`monopoly.py` generates 44x44 stocastic matrix `P`, each element representing the probability of moving from one tile to another in Monopoly. Tiles 1 through 40 follow the game board, moving clockwise from go. 41 through 44 represent staying in jail, outside of the board. 

`output.txt` is the output of the script, labeling different proabilities and expected values of landing on all properties. Houses and hotels were not incorporated in the expected rent.
