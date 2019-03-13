# pacmanAgents.py
# ---------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).




from pacman import Directions
from game import Agent
import random
from heuristics import *
import math

class CompetitionAgent(Agent):
    # Initialization Function: Called one time when the game starts
    def registerInitialState(self, state, depth = '2'):
        self.index = 0
        self.depth = int(depth)                                                                       # used to depth limit the expectimax search, default depth is 2

    # GetAction Function: Called with every frame
    def getAction(self, state):
        # TODO: write your algorithm Algorithm instead of returning Directions.STOP
        def max_turn(state, depth):                                                                   # starting from the maxturn. This is the pacman's turn
            legal = state.getLegalPacmanActions()                                                     # consider all the legal moves                                                    
            if len(legal) == 0 or state.isWin() or state.isLose() or depth == self.depth:             # if no legal moves or Win or Lose or the depth is reached then return the evaluation. When the depth is reached make the node as a leaf node.
                return (self.myEvaluation(state), None)                                               # get the evaluation of the state
            
            temp = -(float("inf"))
            final_action = None
            
            for action in legal:
                successor_value = exp_turn(state.generatePacmanSuccessor(action), 1, depth)[0]        #for all the possible successor states apply the exp turn to estimate the chance and get the evaluation of each successor state.
                
                if temp < successor_value:
                    temp, final_action = successor_value, action                                      #find the successor with the maximum score
                    
            return (temp, final_action)                                                               # take action to go to the best successor.
        
        def exp_turn(state, agent, depth):                                                            # exp turn to estimate the value of possible states based on moves of pacman and ghosts.
            
            legal = state.getLegalActions(agent)                                                      # get legal actions
            if len(legal) == 0:                                                               
                return (self.myEvaluation(state), None)                                               #if no legal action possible just return the value of state
            
            temp = 0
            final_action = None
            
            for action in legal:
                if agent == (state.getNumAgents() - 1):                                               # get the total number agents 
                    successor_value = max_turn(state.generateSuccessor(agent, action), depth + 1)[0]  # pacman's turn if the second ghost has called exp - turn
                else:
                    successor_value = exp_turn(state.generateSuccessor(agent, action), agent + 1, depth)[0]  # call exp-turn for the second ghost
                
                p = successor_value/len(legal)                                                        # The probability of getting to the state
                temp = temp + p                                                                       # The total chance of the state
                
            return (temp, final_action)                                                               # return the chance and best action for that state.
        
        return max_turn(state, 0)[1]                                                                  # start estimating from the pacmans current state.
    
    
    def myEvaluation(self, state):
        
        
        newPos = state.getPacmanPosition()                                                           # get the current position of the pacman
        Food = state.getFood()                                                                       # get the grid of the food
        
        
        foodList = [self.manhattanDistance(newPos, f) for f in Food.asList()]                        # calculate the manhattan distance between pellets and pacman
        
        foodScore = 0
        
        for f in foodList:                                                                      
            foodScore += 1.0/float(f)                                                                # pellets which are closer get higher score then pellets which are farther away
            
        
        newGhostStates = state.getGhostStates()                                                     # Getting the ghost states Note: Only used to get the the scared timer so that the pacman dosent run away from the ghosts when they are scared.
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]                  # scared times for making the pacman eat scared ghosts
            
        GhostPositions = state.getGhostPositions()                                                  # getting the positions of the ghosts.
        GhostDistance = [self.manhattanDistance(newPos, g) for g in GhostPositions]                 # calculate the manhattan distance between ghost and pacman.
        GhostDistance.sort()                                                                        # sort the distance to the ghosts
        
        GhostScore = 0
        if min(GhostDistance) == 0:                                                                 # if the ghost is very near give high penalty
            GhostScore = 100000000
        else:
            for g in GhostDistance:                                                                # add to the ghost score
                if g < 3 and g != 0:                                                               # if the ghost if more than distance of 3 ignore the ghost (if the ghost is very near handled earlier, handled divide be zero error)
                    GhostScore + 1.0/g                                                             # nearer the ghost more is the penalty
        
        scaredtimeSum = sum(newScaredTimes)                                                        # take sum of scared times for both ghosts
        
        return state.getScore() + foodScore - 28 * GhostScore + 1.2 * scaredtimeSum                # final score
     
    def manhattanDistance(self, x, y):
        return abs(x[0] - y[0]) + abs(x[1] - y[1])