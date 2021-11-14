# -*- coding: utf-8 -*-
"""
Created on Thu Feb 25 15:47:12 2021

@author: ericr
"""
import numpy as np
import sys
from Node import Node

############################### Search Class ##################################
class Search:
    # Initialize class
    def __init__(self, outfileStub, games=0):
        self.reset()
        self.games =  games
        
        # Set output file names and clear files
        self.outfile_stub = outfileStub
        self.outfile = []
    # end __init__
       
    # reset Search class variables
    def reset(self):
        self.open=[]
        self.SortedList = []
        self.closed=[]
        self.saved = []
    # end reset()
    
    # Append newly expanded nodes, graph search style.
    def appendNewNodes(self, new):
        for i in new:
                addFlag = True
                # Check if on closed list
                for cl in self.closed:
                    if cl.equalState(i.state):
                        addFlag = False
                        break
                    # Check if on open list
                for op in self.open:
                    if op.equalState(i.state):
                        addFlag = False
                        break
                # if not on open or closed, append to open
                if addFlag:
                    self.open.append(i)
    # end appendNewNodes()
        
    # Trace through solution path for output
    def getSolution(self, start):
        cur = self.closed[-1]
        while not cur.equalState(start.state):
            self.SortedList.append(cur)
            cur = cur.getParent()
        self.SortedList = np.flip(self.SortedList)
    # end getSolution()
        
    # Generates empty output file for heuristic number
    def createOutfile(self, heuristic):
        # Open/create heuristic file for output
        self.outfile = self.outfile_stub + str(heuristic) + ".txt"
        open(self.outfile, 'w').close()
    # end createOutfile()
        
    # Print required output to file
    def printSimpleOutputFile(self, start, heuristic, filename):
        g = np.ceil(self.games%5)
        g=5.0 if g==0 else g
        
        with open(filename, 'a') as f:
            print("#########################################\n",                file=f)
            print("Problem: " + str(g) + ", Set: " + str(np.ceil(self.games/5)), file=f)
            print("Initial Config game " + str(self.games) + "\n" + 
                  str(start.state),   file=f)
            #Print Output
            prevGval = 0
            cntr = 1;
            for idx in self.SortedList:
                if (idx.getGVal() > prevGval):
                    prevGval = idx.getGVal()
                # Print action, state, gVal, hManhattan, hDisplaced for each node
                for move in idx.action:
                    if (idx.parent[1] == idx.action[move]):
                        name = move
                # Get Heuristic value for output
                if ( heuristic == 1 ):
                    h = idx.getDisplaced()
                elif ( heuristic == 2 ):
                    h = idx.getManhattan()
                elif ( heuristic == 3 ):
                    h = idx.getManhattan_Displaced()
                elif ( heuristic == 4 ):
                    h = idx.getRandomizedHeuristic()
                
                print("Node: " + str(cntr) + 
                      ", State Matrix:"      + str(idx.state) +
                      ", Action: " + name + 
                      ", Gval: " + str(idx.getGVal()) +
                      ", Hval  : " + str(h) + 
                      ", iterExpanded: " + str(idx.getIterExp()),   file=f)
                cntr+=1
            print("\nBranching Factor: " + str(float(len(self.closed)+len(self.open))/float(len(self.closed))), file=f)
            print("\n#########################################",                file=f)
        f.close()
    # end printSimpleOutputFile()
    
    
    # Main processing function for class Search
    # Process function conducts search algorithm
    def Process(self, start, goal, game_number, heuristic):
        
        self.games = game_number
        # Create starting node
        start = Node(start)
        self.open.append(start)
        
        # Begin loop
        counter = 1
        while True:
            cur = self.open[0]
            cur.setIterExp(counter)
            counter += 1
            # If the difference between current and goal node is 0 we have reached the goal node
            if(cur.equalState(goal)):
                # Need to get the solution, then close nodes
                self.closed.append(cur)
                self.getSolution(start)
                
                break
            
            # Expand more nodes
            new = cur.expand(goal)
                
            # Put current node on closed, remove from open
            self.closed.append(cur)
            del self.open[0]
            
            # Append to list open if state not already in open or closed
            self.appendNewNodes(new)
            
            # Sort current open nodes on heuristics
            if ( heuristic == 1 ):
                # Sort on Heuristic #1
                self.open.sort(key = lambda x:x.gVal+x.hDisplaced, reverse=False)
                
            elif ( heuristic == 2 ):                
                # Sort on Heuristic #2
                self.open.sort(key = lambda x:x.gVal+x.hManhattan, reverse=False)
                    
            elif ( heuristic == 3 ):  
                # Sort on Heuristic #3
                self.open.sort(key = lambda x:x.gVal+x.hManhattan_hDisplaced, reverse=False)
                    
            elif ( heuristic == 4 ):  
                # Sort on Heuristic #4
                self.open.sort(key = lambda x:x.gVal+x.hRandomized, reverse=False)
            else:
                sys.exit("Incorrect Heuristic input. Try 1, 2, 3, or 4")
            
        # Output files
        self.printSimpleOutputFile(start, heuristic, self.outfile)
        
        # Return Branching Factor
        return float(len(self.closed)+len(self.open))/float(len(self.closed))
        
    # end Process()
    
        
    