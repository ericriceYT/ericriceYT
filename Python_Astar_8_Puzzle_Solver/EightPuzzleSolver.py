# -*- coding: utf-8 -*-
"""
Created on Fri Feb 12 01:06:44 2021

@author: ericr
"""
import numpy as np
import csv
from Search import Search
from Tools import Spiralize

############################ EightPuzzleSolver ########################################

def main():
    # Read input file
    inputFile = 'inputFile.txt'
    with open(inputFile, 'r') as file:
        reader = csv.reader(file)
        puzzles = [r for r in reader]
    puzzles = np.array(puzzles)
    puzzles = puzzles.astype(int)
    # Puzzles now assigned as row vectors
    
    # Define goal state
    goalState = Spiralize(9)
    print("Desired output: \n" + str(goalState.reshape(3,3)) + "\n\n")
    
    # Output files
    # Shows:
    #   (1) Starting node
    #   (2) Sorted list of nodes created from expand() with action, state, gval, hManhattan, hDisplaced of each node
    outfileStub = "OutfileHeuristic"      # sorted list using hDisplaced + gVal

    # Create search game object
    p = Search(outfileStub)
    
    branchFactor = []
    
    desiredHeuristics = [1,2,3,4]
    
    # loop over each heuristic
    for heuristic in desiredHeuristics:
        p.createOutfile(heuristic)
        branchFactor2 = []
        
        # loop for each row in input file
        for cntr, game in enumerate(puzzles, start=1):
            l = len(game)
            
            # Input validity check
            assert (np.sqrt(l).is_integer())
            assert (sum(game) == sum(range(0,l)))
            assert (len(np.unique(game)) == l)
            
            #print("Problem #" + str(cntr) + " Initial: \n" + str(game.reshape(3,3)) + "\n")
            
            p.reset()
            branchFactor2.append(p.Process(game, goalState, cntr, heuristic))
            
            #print("Completed a puzzle!")
            #print("#################################\n")
        with open(p.outfile, 'a') as f:
            print("Average Branching Factor: " + str(np.average(branchFactor2)), file=f)
        f.close()
        branchFactor.append(branchFactor2)
    
    print("\t\t\t\t\th1\t\th2\t\th3\t\th4")
    for ii in range(0,3):
        print("Problem steps " + str((ii+1)*5) + ":", end="\t")
        for jj in range(0,len(desiredHeuristics)):
            print("{:.3f}".format(np.average(branchFactor[jj][ii*5:(ii+1)*5])), end ="\t") 
        print()
    
    print("\nAll games complete")
        
# End Main
        
        
if __name__ == "__main__":
    main()