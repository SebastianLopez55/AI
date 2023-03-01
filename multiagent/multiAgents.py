# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent
from pacman import GameState

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState: GameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState: GameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        # newPos: Pacman position after moving
        newPos = successorGameState.getPacmanPosition()
        # newFood: grid of booleans representing food locations
        newFood = successorGameState.getFood()
        # newGhostStates: list containing objects of GhostStates
        newGhostStates = successorGameState.getGhostStates()
        # newScaredTimes: list representing time left ghost is scared -> list
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]        
        "*** YOUR CODE HERE ***"    

        """
        Variable declarations
        """
        # Get food remaining -> int
        foodRemaining = successorGameState.getNumFood()
        # Get capsule remaining. "Big food" -> list
        capsulesRemaining = successorGameState.getCapsules()
        # calculate furthest distance to food remaining -> int
        farthestFoodDis = max([manhattanDistance(newPos, food) for food in newFood.asList()], default=0)
        # Calculate closest distance to food remaining -> int
        closestFoodDis = min([manhattanDistance(newPos, food) for food in newFood.asList()], default=0)
        # Calculate distance to ghosts - > list
        ghostDistances = [manhattanDistance(newPos, ghost.getPosition()) for ghost in newGhostStates]

        """
        Logic for the heuristics
        """

        # Food heuristic 
        if foodRemaining == 0:
            foodHeuristic = 1000
        else:
            foodHeuristic = (1/closestFoodDis) - (10*foodRemaining)
            
        # Ghost heuristic
        if min(ghostDistances) < 2:
            ghostHeuristic = -5000
        else:
            ghostHeuristic = 0    

        # Final score calculation
        finalScore = foodHeuristic + ghostHeuristic 
                            
        return finalScore

def scoreEvaluationFunction(currentGameState: GameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
         #Maximizer
        def maximizer(gameState :  GameState, depth : int):
            depth += 1
            if gameState.isWin() or gameState.isLose() or depth == self.depth:
                return self.evaluationFunction(gameState)
            branches = [float('-inf')]
            for pac_action in gameState.getLegalActions(0):
                successorState = gameState.generateSuccessor(0, pac_action)
                branches.append(minimizer(successorState, depth, 1))
            return max(branches)

        
        #Minimizer
        def minimizer(gameState : GameState, depth : int, ghost_index : int):
            if gameState.isWin() or gameState.isLose():
                return self.evaluationFunction(gameState)
            ghost_branch = [float('inf')]
            if ghost_index == gameState.getNumAgents()-1:
                for ghost_action in gameState.getLegalActions(ghost_index):
                    successorState = gameState.generateSuccessor(ghost_index, ghost_action)
                    ghost_branch.append(maximizer(successorState, depth))
                return min(ghost_branch)
            else:
                for ghost_action in gameState.getLegalActions(ghost_index):
                    successorState = gameState.generateSuccessor(ghost_index, ghost_action)
                    ghost_branch.append(minimizer(successorState, depth, ghost_index+1))
                return min(ghost_branch)

        #Zero-depth
        score = float('-inf')
        best_action = None
        for pac_action in gameState.getLegalActions(0):
            successorState = gameState.generateSuccessor(0, pac_action)
            new_score = minimizer(successorState, 0, 1)
            if new_score > score:
                score = new_score
                best_action = pac_action
        return best_action
        

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
       #Maximizer
        def maximizer(gameState :  GameState, depth : int, alpha : float, beta: float):
            depth += 1
            if gameState.isWin() or gameState.isLose() or depth == self.depth:
                return self.evaluationFunction(gameState)
            branches = [float('-inf')]
            v = float('-inf')
            for pac_action in gameState.getLegalActions(0):
                successorState = gameState.generateSuccessor(0, pac_action)
                successorScore = minimizer(successorState, depth, 1, alpha, beta)
                v = max(successorScore, v)
                if v > beta:
                    return v
                alpha = max(alpha, v)
                branches.append(successorScore)
            return max(branches)

        
        #Minimizer
        def minimizer(gameState : GameState, depth : int, ghost_index : int, alpha: float, beta: float):
            if gameState.isWin() or gameState.isLose():
                return self.evaluationFunction(gameState)
            ghost_branch = [float('inf')]
            if ghost_index == gameState.getNumAgents()-1:
                v = float('inf')
                for ghost_action in gameState.getLegalActions(ghost_index):
                    successorState = gameState.generateSuccessor(ghost_index, ghost_action)
                    successorScore = maximizer(successorState, depth, alpha, beta)
                    v =  min(successorScore, v)
                    if v< alpha:
                        return v
                    beta = min(beta, v)
                    ghost_branch.append(successorScore)
                return min(ghost_branch)
            else:
                v = float('inf')
                for ghost_action in gameState.getLegalActions(ghost_index):
                    successorState = gameState.generateSuccessor(ghost_index, ghost_action)
                    successorScore = minimizer(successorState, depth, ghost_index+1, alpha, beta)
                    v =  min(successorScore, v)
                    if v< alpha:
                        return v
                    beta = min(beta, v)
                    ghost_branch.append(successorScore)
                return min(ghost_branch)

        #Zero-depth
        alpha = float('-inf')
        beta = float('inf')
        score = float('-inf')
        best_action = None
        v = float('-inf')
        for pac_action in gameState.getLegalActions(0):
            successorState = gameState.generateSuccessor(0, pac_action)
            new_score = minimizer(successorState, 0, 1, alpha, beta)
            if new_score > score:
                score = new_score
                best_action = pac_action
            v = max(new_score, v)
            if v > beta:
                return best_action
            alpha = max(alpha, v)
        return best_action

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
         #Maximizer
        def maximizer(gameState :  GameState, depth : int):
            depth += 1
            if gameState.isWin() or gameState.isLose() or depth == self.depth:
                return self.evaluationFunction(gameState)
            branches = [float('-inf')]
            for pac_action in gameState.getLegalActions(0):
                successorState = gameState.generateSuccessor(0, pac_action)
                branches.append(averager(successorState, depth, 1))
            return max(branches)

        
        #Averager
        def averager(gameState : GameState, depth : int, ghost_index : int):
            if gameState.isWin() or gameState.isLose():
                return self.evaluationFunction(gameState)
            legal_actions = gameState.getLegalActions(ghost_index)
            nbr_actions = len(legal_actions)
            if nbr_actions == 0:
                    return 0
            ghost_value = 0
            if ghost_index == gameState.getNumAgents()-1:
                for ghost_action in legal_actions:
                    successorState = gameState.generateSuccessor(ghost_index, ghost_action)
                    new_value = maximizer(successorState, depth)
                    ghost_value += new_value
                return ghost_value/nbr_actions
            else:
                for ghost_action in legal_actions:
                    successorState = gameState.generateSuccessor(ghost_index, ghost_action)
                    new_value = averager(successorState, depth, ghost_index+1)
                    ghost_value += new_value
                return ghost_value/nbr_actions

        #Zero-depth
        score = float('-inf')
        best_action = None
        for pac_action in gameState.getLegalActions(0):
            successorState = gameState.generateSuccessor(0, pac_action)
            new_score = averager(successorState, 0, 1)
            if new_score > score:
                score = new_score
                best_action = pac_action
        return best_action
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState: GameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """

    # newPos: Pacman position after moving
    newPos = currentGameState.getPacmanPosition()
    # newFood: grid of booleans representing food locations
    newFood = currentGameState.getFood()
    # newGhostStates: list containing objects of GhostStates
    newGhostStates = currentGameState.getGhostStates()
    # newScaredTimes: list representing time left ghost is scared -> list
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]        
    "*** YOUR CODE HERE ***"    

    """
    Variable declarations
    """
    # Get food remaining -> int
    foodRemaining = currentGameState.getNumFood()
    # Get capsule remaining. "Big food" -> list
    capsulesRemaining = currentGameState.getCapsules()
    # calculate furthest distance to food remaining -> int
    lst_food_dist = [manhattanDistance(newPos, food) for food in newFood.asList()]
    farthestFoodDis = max(lst_food_dist, default=0)
    # Calculate closest distance to food remaining -> int
    closestFoodDis = min(lst_food_dist, default=0)
    # Calculate distance to ghosts - > list
    ghostDistances = [manhattanDistance(newPos, ghost.getPosition()) for ghost in newGhostStates]


    """
    Logic for the heuristics
    """
    if currentGameState.isWin():
        return float('inf')
    if currentGameState.isLose():
        return float('-inf')
    

    # Food heuristic

    foodHeuristic =  (1/closestFoodDis) - (10*foodRemaining)
        
    # Ghost heuristic

    if min(ghostDistances) < 2:
        ghostHeuristic = float('-inf')
    elif min(ghostDistances) < 3:
        ghostHeuristic = -100
    else:
        ghostHeuristic = 0

    scared_score = 0
    if len(newScaredTimes) > 0:
        scared_score = sum(newScaredTimes)*2
        ghostHeuristic = 0


    # Final score calculation
    finalScore = currentGameState.getScore() + foodHeuristic + ghostHeuristic + scared_score
        
    return finalScore


# Abbreviation
better = betterEvaluationFunction