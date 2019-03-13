# heuristic for selecting the node
def scoreEvaluation(state):
    return state.getScore() + [0,-1000.0][state.isLose()] + [0,1000.0][state.isWin()]

def normalizedScoreEvaluation(rootState, currentState):
    rootEval = scoreEvaluation(rootState);
    currentEval = scoreEvaluation(currentState);
    return (currentEval - rootEval) / 1000.0;

# heuristic (remaining cost) for A*
def admissibleHeuristic(state):
    if state.isLose():
        return 1000.0;
    return state.getNumFood() + len(state.getCapsules());

def manhattanDistance(x1, x2):
    return abs(x1[0] - x2[0]) + abs(x1[1] - x2[1])

def betterEvaluation(state):
    pos = state.getPacmanPosition()
    current_score = scoreEvaluation(state)
    
    if state.isLose():
        return -float("inf")
    elif state.isWin():
        return float("inf")
    
    foodList = state.getFood().asList()
    manhattanDistancetoClosestFood = min(map(lambda x:manhattanDistance(pos, x), foodList))
    dist = manhattanDistancetoClosestFood
    
    numberOfCapsulesLeft = len(state.getCapsules())
    
    numberOfFoodsLeft = len(foodList)
    
    scaredGhosts, activeGhosts = [], []
    for ghost in state.getGhostStates():
        if not ghost.scaredTimer:
            activeGhosts.append(ghost)
        else:
            scaredGhosts.aapend(ghost)
    
    distanceToClosestActiveGhost = distanceToClosestScaredGhost = 0
    
    if activeGhosts:
        distanceToClosestActiveGhost =  min(map(lambda g:manhattanDistance(pos, g.getPosition()), activeGhosts))
    else:
        distanceToClosestActiveGhost = float("inf")
    distanceToClosestActiveGhost = max(distanceToClosestActiveGhost, 5)
    
    if scaredGhosts:
        distanceToClosestScaredGhost = min(map(lambda g:manhattanDistance(pos, g.getPosition()), scaredGhosts))
    else:
        distanceToClosestScaredGhost = 0
    
    score = 1 * current_score + \
            -1.5 * dist + \
            -2 * (1/distanceToClosestActiveGhost) + \
            -2 * distanceToClosestScaredGhost + \
            -20 * numberOfCapsulesLeft + \
            -4 * numberOfFoodsLeft
    
    return score