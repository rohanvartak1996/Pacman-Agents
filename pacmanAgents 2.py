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
from heuristics import *
import random
import math


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

class RandomSequenceAgent(Agent):
    # Initialization Function: Called one time when the game starts
    def registerInitialState(self, state):
        self.actionList = [];
        for i in range(0,10):
            self.actionList.append(Directions.STOP);
        return;

    # GetAction Function: Called with every frame
    def getAction(self, state):
        # get all legal actions for pacman
        possible = state.getAllPossibleActions();
        for i in range(0,len(self.actionList)):
            self.actionList[i] = possible[random.randint(0,len(possible)-1)];
        tempState = state;
        for i in range(0,len(self.actionList)):
            if tempState.isWin() + tempState.isLose() == 0:
                tempState = tempState.generatePacmanSuccessor(self.actionList[i]);
            else:
                break;
        # returns random action from all the valide actions
        return self.actionList[0];

class HillClimberAgent(Agent):
    # Initialization Function: Called one time when the game starts
    def registerInitialState(self, state):
        self.actionList = [];
        for i in range(0,5):
            self.actionList.append(Directions.STOP);
        return;

    # GetAction Function: Called with every frame
    def getAction(self, state):
        # TODO: write Hill Climber Algorithm instead of returning Directions.STOP
        
        if state.isWin():
            return Directions.STOP
    
        new_eval = 0
        action_sequence = []
        possible = state.getAllPossibleActions()          # getting all the possible actions
        for i in range(0, 5):
            action_sequence.append(possible[random.randint(0, len(possible)-1)])  #generating an action sequence
        fstate = state
        lstate = state
        for action in action_sequence:                      # going through the sequence to get to the final state for the first time 
            if lstate.isWin() + lstate.isLose() == 0:
                lstate = lstate.generatePacmanSuccessor(action)
            else:
                break;
        first_eval = gameEvaluation(fstate, lstate)     # game evaluation for the action sequence for first time
        # Now evolving the action sequence
        while lstate:                                      #continue while the entire action sequence is being evaluated
            new_action_seq = action_sequence               # taking the action sequence
            for i in range (0, len(new_action_seq)-1):              
                if random.uniform(0, 1) > 0.5:               # with probability of 0.5 changing each action in the sequence with any                                                  random action
                    new_action_seq[i] = possible[random.randint(0, len(possible)-1)]
                else:
                    pass
        
            for action in new_action_seq:                          # evaluating the action sequence
                if lstate.isWin() + lstate.isLose() == 0:
                    lstate = lstate.generatePacmanSuccessor(action)   # generating successor
                else:
                    lstate = None                                    # if successor cannot be generated stop
                    break
            if lstate:                                          
                new_eval = gameEvaluation(fstate, lstate)
            if new_eval > first_eval:                           # check if the new sequence is better than the previous one
                action_sequence = new_action_seq                # if better use the new sequence
            else:
                pass                                            # else use the same sequence
        
        return action_sequence[0]                               # return the first action of the last evolved sequence
    

class GeneticAgent(Agent):
    # Initialization Function: Called one time when the game starts
    def registerInitialState(self, state):
        return;

    # GetAction Function: Called with every frame
    def getAction(self, state):
        # TODO: write Genetic Algorithm instead of returning Directions.STOP
        
        if state.isWin():
            return Directions.STOP
        
        population = []
        possible = state.getAllPossibleActions()
        
        for i in range(0, 8):                     # generating a population with 8 individuals
            act_seq = []
            for j in range(0, 5):
                act_seq.append(possible[random.randint(0, len(possible)-1)])
            population.append([act_seq,0])
            
        fstate = state
        lstate = state
        breaker = None
        f_action = None
        
        while lstate:               #continue while the entire action sequence is being evaluated
        
            for pop in population:       # for each individual in population evaluate the action sequence
                for action in pop:
                    if lstate.isWin() + lstate.isLose() == 0:
                        lstate = lstate.generatePacmanSuccessor(action)
                    else:
                        
                        breaker = True                 # if the successor cannot be generated then stop
                        break                          # breaking the inner for loop
                    
                if breaker:                            # breaking the outer for loop
                    break
                if lstate:
                    new_eval = gameEvaluation(fstate, lstate)    # evaluate the individual
                    pop[1] = new_eval                            # store the fitness of the individual
            
            if breaker:                                          # breaking the while loop if successor cannot be generated
                break 
        
            population = sorted(population, key=lambda p:p[1], reverse=True)  # sorting the population according to fitness
            f_action = population[0][0][0]          # first action of the best individual of the population
        
            roulette_wheel = []                           # creating a roulette wheel
            x = 0
            y = 8
            for z in range(0, 8):                         # roulette wheel where higher fitness has higher area 
                roulette_wheel = roulette_wheel + [x]*y   # 0 will be 8 time, 1 will be 7 times and so on
                x = x + 1                                 # the most fit individual is a 0 in population 
                y = y - 1                                 # the individual with more number of index in roulette wheel has higher                                                 chance of getting selected   # tm2491@nyu.edu
        
            new_population = []
            for it in range(0, 4):                        # generating 8 children, 2 from each pair of parents
                #print("In crossover",it)
                parent1 = random.choice(roulette_wheel)     # choosing 1st parent
                parent2 = random.choice(roulette_wheel)     # choosing 2nd parent
                
                chromosome1 = population[parent1][0]        #chromosomes for each parent
                chromosome2 = population[parent2][0]
                
                #print("Lengthof ch1",len(chromosome1))
                #print("Length of ch2",len(chromosome2))
            
                if random.uniform(0, 1) < 0.7:                # cross over with probability of 0.7
                    offspring1 = []
                    offspring2 = []
                    for i in range(0, 5):                       # random test for selecting the gene
                        if random.uniform(0, 1) < 0.5:           # if less than 50% genes selected from parent 1
                            offspring1.append(chromosome1[i])
                            offspring2.append(chromosome1[i])
                        else:                                    # if more than 50% genes selected from parent 2
                            offspring1.append(chromosome2[i])
                            offspring2.append(chromosome2[i])
                
                    new_population.append([offspring1,0])       # add offsprings to new population
                    new_population.append([offspring2,0])
                else:
                    new_population.append([chromosome1,0])     # add parents to new population without crossover
                    new_population.append([chromosome2,0])
            
            #for pop in new_population:                          # Mutation with probability of 0.1
                #if random.uniform(0, 1) < 0.1:
                    #pop[0][random.randint(0,4)] = possible[random.randint(0, len(possible)-1)]
                    
            population = new_population            
            
        return f_action            # return the first action of the best individual of the last generated population
        
    
            
                
            
        
                 

class MCTSAgent(Agent):
    # Initialization Function: Called one time when the game starts
    
    
    
    def registerInitialState(self, state):
        global action_list
        global Q
        global N
        global parent
        global children
        
        self.possible = state.getAllPossibleActions()
        action_list = dict()                            # to store actions
        Q = dict()                                        # to store the value of Q
        N = dict()                                       # to store the value of N
        parent = dict()                                 # to store the parent of the node
        children = dict()                               # to store the children of the node
        return;
    
    def defaultPolicy(self, state):
        
        fstate = state
        lstate = state
        
        for _ in range(0, 5):                           # action sequence of 5 five actions
            action = self.possible[random.randint(0, len(self.possible)-1)]
            if lstate.isWin() + lstate.isLose() == 0:              # if the successor can be generated 
                lstate = lstate.generatePacmanSuccessor(action)     # to not next state
            else:
                return None                                         # else return none when successor cannot be generated
        return gameEvaluation(fstate, lstate)
    
    def expand(self, state):
        
        if state not in action_list.keys():                    # generating all possible actions  
            legal = state.getLegalPacmanActions()               # getting the legal actions for the node
            act_list = []
            for action in legal:
                act_list.append(action)                         # putting the actions into the list
            action_list[state] = act_list
            
        new_action = action_list[state].pop(0)                  # select an untried action
        if state.isWin() + state.isLose() == 0:
            new_state = state.generatePacmanSuccessor(new_action)   # generate the next node
        else:
            return None                     # if the next node cannot be generated return None (computational budget)
        Q[new_state] = 0.0                                      # enter Q and N
        N[new_state] = 0.0
        parent[new_state] = state                               # enter parent for new node
        if state not in children.keys():                        # add new node into children of previous node
            children[state] = []
        children[state].append((new_state,new_action))          # return the new node
        
        return new_state
    
    def best_child(self, state):
        children_list = children[state]
        m = 0
        k = 0
        temp = None
        for child in children_list:                # from the children select the best child based on formula
            k = ((Q[child[0]]/N[child[0]])+math.sqrt((2*math.log(N[state]))/N[child[0]]))
            if m < k:
                m = k
                temp = child
            
        return temp[0]
    
    def tree_policy(self, state):
            if state not in action_list.keys():   # expanding for the first time(all possible children will get added to list)
                return self.expand(state)          # applying expand
            elif action_list[state] != []:        # while the node is not fully expanded continue to expand
                return self.expand(state)
            else:
                v = self.best_child(state)          # else returning the best child
                return v
       
    
    def backup(self, v, delta):                     # backing up value of Q and N
        while v is not None:
            N[v] = N[v] + 1
            Q[v] = Q[v] + delta
            v = parent[v]
        
             
    
        
        

    # GetAction Function: Called with every frame
    def getAction(self, state):
        # TODO: write MCTS Algorithm instead of returning Directions.STOP
        
        if state.isWin():
            return Directions.STOP
        
        N[state] = 0.0                # initializations for the starting state
        Q[state] = 0.0
        parent[state] = None
        delta = 1
        tempState = state                   # starting state
        v = 1
        while delta and v:                          # stopping condition (computational budget- while the successor can be generated)
            #print("In MCTS")
            v = self.tree_policy(tempState)      # applying tree policy
            if v == None:                        # if successor cannot be generated stop
                break
            delta = self.defaultPolicy(v)        # applying delta- gives stopping conidition
            if delta == None:                    # if successor cannot be generated stop
                break
            self.backup(v, delta)               # back up
            
        
        children_list = children[state]
        m = 0
        act = None 
        for child in children_list:           # finding the valut of  Max N (Most visited node)
            if m < N[child[0]]:
                m = N[child[0]]
        
        cl = [] 
        for child in children_list:           # finding all the children with Max N
            if N[child[0]] == m:
                cl.append(child)
        
        if len(cl) == 1:                     # if only one child return action corresponding to it 
            act = cl[0][1]
        else:                                 # if multiple children with max N
            t = random.randint(0, len(cl)-1)  # break ties randomly
            act = cl[t][1]                     # select action from randomly selected child
        
                
        return act             # returing action to go to most visited node

                
