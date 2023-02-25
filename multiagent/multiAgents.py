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
        if min(ghostDistances) < 3:
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


        """
        self.depth -> 2
        gameState.getLegalActions(0) -> ['Left', 'Right']
        """

        print("\n============   START 0F PRINT STATEMENTS FOR TESTING ============ \n\n")
    
        print("\n\n============   ENDS 0F PRINT STATEMENTS FOR TESTING ============  \n")
    
        def minimax(gameState, depth, agentIndex):
            # Check if state is a terminal state: return the state's utility
            if gameState.isWin() or gameState.isLose():
                return self.evaluationFunction(gameState)

            # Check if depth is reached
            if depth == self.depth:
                return self.evaluationFunction(gameState)

            # Check if the agent is MAX: return max-value(state)
            if agentIndex == 0:
                return max_value(gameState, depth, agentIndex)

            # Check if agent is MIN: return min-value(state)
            if agentIndex > 0:
                return min_value(gameState, depth, agentIndex)

        def max_value(gameState, depth, agentIndex):
            return minimax(gameState, depth + 1, agentIndex + 1)
            
        def min_value(gameState, depth, agentIndex):
            # Check if we already reach the last ghost: reset to Pacman
            if gameState.getNumAgents() == agentIndex:
                return minimax(gameState, depth + 1, 0)
            return minimax(gameState, depth, agentIndex + 1)

        return minimax(gameState, 0, 0)
        util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

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
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState: GameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
