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
from game import Actions
from heuristics import *
import random

class RandomAgent(Agent):
    # Initialization Function: Called one time when the game starts
    def registerInitialState(self, state):
        return;

    # GetAction Function: Called with every frame
    def getAction(self, state):
        # get all legal actions for pacman
        actions = state.getLegalPacmanActions()
        # returns random action from all the valide actions
        return actions[random.randint(0,len(actions)-1)]

class OneStepLookAheadAgent(Agent):
    # Initialization Function: Called one time when the game starts
    def registerInitialState(self, state):
        return;

    # GetAction Function: Called with every frame
    def getAction(self, state):
        # get all legal actions for pacman
        legal = state.getLegalPacmanActions()
        # get all the successor state for these actions
        successors = [(state.generatePacmanSuccessor(action), action) for action in legal]
        # evaluate the successor states using scoreEvaluation heuristic
        scored = [(admissibleHeuristic(state), action) for state, action in successors]
        # get best choice
        bestScore = min(scored)[0]
        # get all actions that lead to the highest score
        bestActions = [pair[1] for pair in scored if pair[0] == bestScore]
        # return random action from the list of the best actions
        return random.choice(bestActions)    
    
    
    
class BFSAgent(Agent):
    
    
    
    def registerInitialState(self, state):
        return;
        
    

    # GetAction Function: Called with every frame
    def getAction(self, state):
        # TODO: write BFS Algorithm instead of returning Directions.STOP
       
        q = []                                 # queue to store the elements 
        visited = []                           # visited to keep track of explored nodes
        p_info = dict()                        # to keep the actions to go from root node to a particular node
        total_cost_info = dict()                # to keep the total cost of the node
        
        
        q.append(state)                    # putting the statring node in queue
        p_info[state] = []
        total_cost_info[state] = 0
        best_node = None
        best_node_cost = 100000
        k = 1
        
        while q:
            
            s = q.pop(0)                # pop the first node from the queue
            if s == None:
                continue
             
            
            visited.append(s)   
            legal = s.getLegalPacmanActions()
            successors = [(s.generatePacmanSuccessor(action), action) for action in legal]  #generate all successor of the node
            for suc in successors:
                if suc[0] not in visited:        # if the successor is not already visited and not in queue
                    if suc[0] is None:        # if successor id none then node is leaf node, calculating the best leaf node.
                        if total_cost_info[s] < best_node_cost :
                            best_node = s
                            best_node_cost = total_cost_info[s]
                    else:
                        q.append(suc[0])                      # put the successor in queue
                        p_info[suc[0]] = []                   # put information of actions to reach the successor
                        p_info[suc[0]].extend(p_info[s])
                        p_info[suc[0]].append(suc[1])
                        total_cost_info[suc[0]] = 1 + total_cost_info[s] + admissibleHeuristic(s)  #total cost of the node.
        
        l = p_info[best_node]
        act = l[0]                     # return single action that leads to best node
        
        return act
            
            

class DFSAgent(Agent):
    
    
    
    
    
    # Initialization Function: Called one time when the game starts
    def registerInitialState(self, state):
        return;

    # GetAction Function: Called with every frame
    def getAction(self, state):
        # TODO: write DFS Algorithm instead of returning Directions.STOP
        q = []                                 # array to store the elements which will pe used as stack
        visited = []                           # visited to keep track of explored nodes
        p_info = dict()                        # to keep the actions to go from root node to a particular node
        total_cost_info = dict()                # to keep the total cost of the node
        
        
        q.append(state)                    # putting the statring node in stack
        p_info[state] = []
        total_cost_info[state] = 0
        best_node = None
        best_node_cost = 100000
        
        while q:
            
            s = q.pop()                # pop the last node from the stack
            if s == None:
                continue
            
            
            visited.append(s)   
            legal = s.getLegalPacmanActions()
            successors = [(s.generatePacmanSuccessor(action), action) for action in legal]  #generate all successor of the node
            for suc in successors:
                if suc[0] not in visited:     # if the successor is not already visited
                    if suc[0] is None:        # if successor id none then node is leaf node, calculating the best leaf node.
                        if total_cost_info[s] < best_node_cost :
                            best_node = s
                            best_node_cost = total_cost_info[s]
                    else:
                        q.append(suc[0])                      # put the successor in stack
                        p_info[suc[0]] = []                   # put information of actions to reach the successor
                        p_info[suc[0]].extend(p_info[s])
                        p_info[suc[0]].append(suc[1])
                        total_cost_info[suc[0]] = 1 + total_cost_info[s] + admissibleHeuristic(s)  #total cost of the node.
        
        l = p_info[best_node]
        act = l[0]                     # return single action that leads to best node
       
        return act

class AStarAgent(Agent):
    # Initialization Function: Called one time when the game starts
    def registerInitialState(self, state):
        return;

    # GetAction Function: Called with every frame
    def getAction(self, state):
        q = []                                 # queue to store the elements
        visited = []                           # visited to keep track of explored nodes
        p_info = dict()                        # to keep the actions to go from root node to a particular node
        total_cost_info = dict()                # to keep the total cost of the node
        
        
        q.append((state,0))                    # putting the statring node in queue
        p_info[state] = []
        total_cost_info[state] = 0
        best_node = None
        best_node_cost = 100000
        
        while q:
            
            q.sort(key = lambda q:q[1])    #sorting the queue
            s = q.pop(0)[0]                # pop the first node from queue 
            if s == None:
                continue
            
            if s not in visited:
                visited.append(s)   
                legal = s.getLegalPacmanActions()
                successors = [(s.generatePacmanSuccessor(action), action) for action in legal]  #generate all successor of the node
                for suc in successors:
                    if suc[0] is None:        # if successor id none then node is leaf node, calculating the best leaf node.
                        if total_cost_info[s] < best_node_cost :
                            best_node = s
                            best_node_cost = total_cost_info[s]
                    else:
                        total_cost_info[suc[0]] = 1 + total_cost_info[s] + admissibleHeuristic(s)  #total cost of the node.
                        t = total_cost_info[suc[0]]
                        q.append((suc[0],t))                      # put the successor and total cost in queue
                        p_info[suc[0]] = []                   # put information of actions to reach the successor
                        p_info[suc[0]].extend(p_info[s])
                        p_info[suc[0]].append(suc[1])
                        
                        
        l = p_info[best_node]
        act = l[0]                     # return single action that leads to best node
       
        return act
