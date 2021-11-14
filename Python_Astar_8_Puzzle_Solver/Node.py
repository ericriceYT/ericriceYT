# -*- coding: utf-8 -*-
"""
Created on Thu Feb 25 15:48:36 2021

@author: ericr
"""
import numpy as np
############################ Node Class #######################################
class Node:
    
    # Define dict for action labels
    
    ## Initialize class Node
    def __init__(self, state, parent=np.zeros(2), gVal=0, children=[]):
        self.state      = state             # Number locations on board
        self.parent     = parent            # Parent, action
        self.hDisplaced = 0                 # Number of tiles not in desired locations
        self.hManhattan = 0                 # Sum of block distances to desired locations
        self.hManhattan_hDisplaced = 0      # Sum of block distances to desired locations + tiles not in desired location
        self.hRandomized = 0                # Randomized heuristic of either dManhattan of 1-3 or dManhattan of 5-7
        self.gVal       = gVal              # gVal of parent +1 (depth counter)
        self.children   = children          # This is a 2 element array list of action/node pairs
        self.iterExp    = 0                 # Iteration node is expanded
        self.size       = int(np.sqrt(len(state)))
        self.action = {"Up":-self.size, "Left":-1, "Right":1, "Down":self.size}
    # end __init__

    # Method equalState() compares two nodes, returns bool for comparrison
    def equalState(self, state2):
        return (self.state==state2).all()
    # end equalState()
    
    
    # Method expand() computes children of node, creates node object for each child created
    def expand(self, goalState):
        idx = np.where(self.state.reshape(self.size,self.size) == 0)
        row, col = idx[0], idx[1]
        
        # Put logic to expand here, including action test
        children = []
        for move in self.action:
            moveFlag = self.checkMoveValid(move, row, col)
                
            if (moveFlag==True): 
                temp = np.copy(self.state)
                child = self.generateChild(temp, move, goalState)
                children.append(child)
                self.children.append((move, child))
        return children
    # end expand()
    
    
    def checkMoveValid(self, move, row, col):
        moveFlag = False
        # Dont expand into parent node
        if (self.action[move] == -self.parent[1]):
            pass      
        # Dont expand outside of game bounds
        elif (move == "Up" and row > 0):
            moveFlag = True
        elif (move == "Down" and row < self.size-1):
            moveFlag = True
        elif (move == "Left" and col > 0):
            moveFlag = True
        elif (move == "Right" and col < self.size-1):
            moveFlag = True
        return moveFlag
    # checkMoveValid()
        
    def generateChild(self, state, move, goalState):
        child_node = Node(state, np.array((self, self.action[move])), self.getGVal()+1)
        child_node.doAction()
        child_node.setDisplaced(child_node.calcDisplaced(goalState))
        child_node.setManhattan(child_node.calcManhattan(goalState))
        child_node.setManhattan_Displaced(child_node.calcManhattan_Displaced(goalState))
        child_node.setRandomizedHeuristic(child_node.calcRandomizedHeuristic(goalState))
        
        return child_node
    # end generateChild()
    
    # generates result of action without assigning to node
    def simAction(self, state, move):
        x = np.where(state == 0)[0]
        x2 = x+self.action[move]
        state[x] = state[x2]
        state[x2] = 0
        return state
    # end simAction()
        
    # Generates new node with given action
    def doAction(self):
        x = np.where(self.state == 0)[0]
        x2 = x+self.parent[1]
        self.state[x] = self.state[x2]
        self.state[x2] = 0
    # end doAction()
    
    
    # Function to get Hueristics
    def calcDisplaced(self, goalState):
        # Calc number of displaced values
        return np.max((np.count_nonzero((self.state-goalState))-1, 0))
    # end calcDisplaced()
        
    
    # calc manhattan distance
    def calcManhattan(self, goalState):
        temp=0
        for val in range(1, len(self.state)):
            x1, y1 = np.where(self.state.reshape(self.size, self.size) == val)
            x2, y2 = np.where(goalState.reshape(self.size, self.size)== val)
            temp += abs(x1-x2)+abs(y1-y2)
        return temp[0]
    # end calcManhattan()
        
    
    # calc manhattan distance + displaced
    def calcManhattan_Displaced(self, goalState):
        return (self.calcManhattan(goalState) + self.calcDisplaced(goalState))
# end calcManhattan_Displaced()
    
    # calc randomized Heuristic
    # Calculates manhattan distance of first row, manhattan distance of second row, 
    # and randomly returns one of them
    def calcRandomizedHeuristic(self, goalState):
        randManh1=0
        for val in self.state[0:3]:
            if not val == 0:
                x1, y1 = np.where(self.state.reshape(self.size, self.size) == val)
                x2, y2 = np.where(goalState.reshape(self.size, self.size)== val)
                randManh1 += abs(x1-x2)+abs(y1-y2)
        randManh2=0
        for val in self.state[3:6]:
            if not val == 0:
                x1, y1 = np.where(self.state.reshape(self.size, self.size) == val)
                x2, y2 = np.where(goalState.reshape(self.size, self.size)== val)
                randManh2 += abs(x1-x2)+abs(y1-y2)
                
        rVal = np.random.uniform(0, 1, 1)
        if rVal > 0.5:
            return randManh1[0]
        else:
            return randManh2[0]
    # end calcRandomizedHeuristic()

        
    ### Getter and Setter functions. Not really used much ###
    # State
    def getState(self):
        return self.state
    
    def setState(self, newState):
        self.state = newState
        
    # parent
    def getParent(self):
        return self.parent[0]
    
    def setParent(self, newParent):
        self.parent = newParent
        
    # hDisplaced
    def getDisplaced(self):
        return self.hDisplaced
    
    def setDisplaced(self, newDisplaced):
        self.hDisplaced = newDisplaced
        
    # hManhattan
    def getManhattan(self):
        return self.hManhattan
    
    def setManhattan(self, newManhattan):
        self.hManhattan = newManhattan
        
    # hManhattan_hDisplaced
    def getManhattan_Displaced(self):
        return self.hManhattan_hDisplaced
    
    def setManhattan_Displaced(self, newhManhattan_hDisplaced):
        self.hManhattan_hDisplaced = newhManhattan_hDisplaced
        
    # get RandomizedHeuristic
    def getRandomizedHeuristic(self):
        return self.hRandomized
    
    def setRandomizedHeuristic(self, newhRandomized):
        self.hRandomized = newhRandomized
        
    # gVal
    def getGVal(self):
        return self.gVal
    
    def setGVal(self, newGVal):
        self.gVal = newGVal
        
    # iterExp
    def getIterExp(self):
        return self.iterExp
    
    def setIterExp(self, iterNew):
        self.iterExp = iterNew
        
        