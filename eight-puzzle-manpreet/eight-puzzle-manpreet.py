"""
Name: Manpreet Bahl
Python Version: 3.5.2

This program is solves the 8-puzzle problem using
both BFS and A* algorithm.

In order to run this program, type the following
command:
    python3 solver.py

Since the output stream is large, it's better to
redirect it to a file. This can be done by the
following command on a Linux machine:
    python3 solver.py > output.txt
"""
#==================Imports===================
import numpy as np 
from scipy.spatial import distance
#============================================

#================Constants===================
MAX_MOVES = 5000
GOAL = np.array([[1,2,3],[4,5,6],[7,8,0]])
#============================================

class Board:
    """
    This class defines the 8 puzzle board state.
    """
    def __init__(self, values=None, state=None):
        """
        This method initializes the Board class.
        It takes either values of the board configuration as a csv string
        or a state which is a numpy array representing the board.
        Parameters:
            1) values: board configuration as csv string
            2) state: board configuration as csv string
        Return:
            1) N/A
        """
        if values:
            self.state = np.fromstring(values, dtype='int', sep=',').reshape(-1,3)
        else:
            self.state = state
        
        #Keep track of parent
        self.parent = None

        #The path cost to reach this current configuration
        self.cost = 0
        
    def __eq__(self, other):
        """
        This method allows for Board objects to be compared
        using the state attribute.
        Parameters:
            1) other: Board object to compare to
        Return:
            1) Boolean value indicating if the two objects are equal
        """
        return np.array_equal(self.state,other.state)

    def __str__(self):
        """
        This method returns a string representation of the Board
        state in a pretty format.
        Parameters:
            1) N/A
        Return:
            1) output: String representation of the Board state
        """
        output = ''
        for i in self.state:
            for j in i:
                output += "{}".format(j).rjust(3)
            output += "\n"
        return output

    def __copy__(self):
        """
        This method creates a clone of the current Board object
        Parameters:
            1) N/A
        Return:
            1) Board object with exact same state values
        """
        return Board(None, self.state)

    def moves(self):
        """
        This method generates all possible moves at a given Board
        configuration.
        Parameters:
            1) N/A
        Return:
            1) possibleMoves: List of Board objects that are possible moves
                              at given Board configuration
        """
        row, column = np.argwhere(self.state == 0)[0]
        possibleMoves = []

        #Generate board states of possible moves at current state
        if row > 0:
            nextState = np.copy(self.state)
            nextState[row - 1][column], nextState[row][column] = self.state[row][column], self.state[row - 1][column]
            move = Board(state=nextState)
            move.cost = self.cost + 1
            possibleMoves.append(move)

        if column > 0:
            nextState = np.copy(self.state)
            nextState[row][column - 1], nextState[row][column] = self.state[row][column], self.state[row][column - 1]
            move = Board(state=nextState)
            move.cost = self.cost + 1
            possibleMoves.append(move)
        
        if row < 2:
            nextState = np.copy(self.state)
            nextState[row + 1][column], nextState[row][column] = self.state[row][column], self.state[row + 1][column]
            move = Board(state=nextState)
            move.cost = self.cost + 1
            possibleMoves.append(move)
        
        if column < 2:
            nextState = np.copy(self.state)
            nextState[row][column + 1], nextState[row][column] = self.state[row][column], self.state[row][column + 1]
            move = Board(state=nextState)
            move.cost = self.cost + 1
            possibleMoves.append(move)
        
        return possibleMoves
    
    def misplacedTiles(self):
        """
        This method implements the misplaced number of tiles heuristic
        where it sums up the number of elements that are not equal to the
        goal state.
        Parameters:
            1) N/A
        Return:
            1) The number of misplaced tiles
        """
        return np.sum(self.state != GOAL)
    
    def manhattan(self):
        """
        This method implements the manhattan distance heuristic where
        it calculates the sum of the amount of moves that each tile
        needs to make in order to reach its goal position.
        Parameters:
            1) N/A
        Return:
            1) dist: Total sum of the amount of moves each tile needs
                     to make in order to reach its goal position
        """
        dist = 0
        for i in range(1,9):
            current = np.argwhere(self.state == i)[0]
            target = np.argwhere(GOAL == i)[0]

            if np.array_equal(current,target) == False:
                dist += distance.cityblock(current, target)
        
        return dist
    
    def euclidean(self):
        """
        This method implements the euclidean distance heuristic where
        the total sum of each tile's euclidean distance is calculated.
        Parameters:
            1) N/A
        Return:
            1) dist: Total sum of the euclidean distance for each tile
        """
        dist = 0
        for i in range(1,9):
            current = np.argwhere(self.state == i)[0]
            target = np.argwhere(GOAL == i)[0]

            if np.array_equal(current,target) == False:
                dist += distance.euclidean(current,target)
    
        return dist
    
    def traversePath(self, path):
        """
        This method traverses the Board's path in order to
        generate the solution path.
        Parameters:
            1) path: empty list to store the traversal information
        Return:
            1) path: filled with the nodes from start to solution
        """
        if self.parent is None:
            return path
        path.insert(0, self)
        return self.parent.traversePath(path)
       
        
def bfs(values, heuristic):
    """
    This method implements the Best First Search.
    Parameters:
        1) values: Board configuration as csv string
        2) heuristic: Which heuristic to use. Possible values
                      are: 'misplaced', 'manhattan', 'euclidean'
    Returns:
        1) Tuple containing the number of states explored and
           the solution node
    """
    #Initialize
    start = Board(values)
    moves = 0
    frontier = []
    explored = []

    frontier.append(start)

    while len(frontier) > 0 and moves <= MAX_MOVES:
        #Remove first node and increment number of states explored by 1
        node = frontier.pop(0)
        moves += 1

        #Is this node the solution?
        if np.array_equal(node.state, GOAL):
            return (moves,node)

        #Add to explored list
        explored.append(node)

        #Generate the neighbors of the current board
        neighbors = node.moves()
        for n in neighbors:
            n.parent = node #Set the link of the neighbors to the current node
            #If neighbor not in explored and not in frontier, add to frontier
            if n not in explored and n not in frontier: 
                frontier.append(n)
            elif n in frontier:
                #Replace node in frontier with neighbor if it has lower cost
                i = frontier.index(n)
                if heuristic == 'misplaced':
                    if frontier[i].misplacedTiles() > n.misplacedTiles():
                        frontier[i] = n
                elif heuristic == 'manhattan':
                    if frontier[i].manhattan() > n.manhattan():
                        frontier[i] = n
                elif heuristic == 'euclidean':
                    if frontier[i].euclidean() > n.euclidean():
                        frontier[i] = n

        #Sort frontier list based on heuristic
        if heuristic == 'misplaced':
            frontier = sorted(frontier, key=lambda x: x.misplacedTiles())
        elif heuristic == 'manhattan':
            frontier = sorted(frontier, key=lambda x: x.manhattan())
        elif heuristic == 'euclidean':
            frontier = sorted(frontier, key=lambda x: x.euclidean())
    return (moves, None)
            

def astar(values, heuristic):
    """
    This method implements the A* search algorithm.
    Parameters:
        1) values: Board configuration as csv string
        2) heuristic: Which heuristic to use. Possible values
                      are: 'misplaced', 'manhattan', 'euclidean'
    Returns:
        1) Tuple containing the number of states explored and
           the solution node
    """
    #Initialize
    start = Board(values)
    moves = 0
    frontier = []
    explored = []

    frontier.append(start)

    while len(frontier) > 0 and moves <= MAX_MOVES:
        #Remove first node and increment number of states explored by 1
        node = frontier.pop(0)
        moves += 1

        #Is this node the solution?
        if np.array_equal(node.state, GOAL):
            return (moves,node)

        #Add to explored list
        explored.append(node)

        #Generate the neighbors of the current board
        neighbors = node.moves()
        for n in neighbors:
            n.parent = node #Set the link of the neighbors to the current 
            #If neighbor not in explored and not in frontier, add to frontier
            if n not in explored and n not in frontier:
                frontier.append(n)
            elif n in frontier:
                #Replace node in frontier with neighbor if it has lower cost. f(n) = g(n) + h(n)
                i = frontier.index(n)
                if heuristic == 'misplaced':
                    if frontier[i].misplacedTiles() + frontier[i].cost > n.misplacedTiles() + n.cost:
                        frontier[i] = n
                elif heuristic == 'manhattan':
                    if frontier[i].manhattan() + frontier[i].cost > n.manhattan() + n.cost:
                        frontier[i] = n
                elif heuristic == 'euclidean':
                    if frontier[i].euclidean() + frontier[i].cost > n.euclidean() + n.cost:
                        frontier[i] = n

        #Sort frontier list based on heuristic and cost to reach that node
        if heuristic == 'misplaced':
            frontier = sorted(frontier, key=lambda x: x.misplacedTiles() + x.cost)
        elif heuristic == 'manhattan':
            frontier = sorted(frontier, key=lambda x: x.manhattan() + x.cost)
        elif heuristic == 'euclidean':
            frontier = sorted(frontier, key=lambda x: x.euclidean() + x.cost)
    return (moves, None)

def main():
    """
    This method defines the main method where it handles the
    initial states and pretty printing the outputs.
    Parameters:
        1) N/A
    Return:
        1) N/A
    """
    def printSolution(solutionPath):
        """
        This method prints the solution path
        Parameters:
            1) solutionPath: The list of nodes to the solution
        Return:
            1) N/A
        """
        for p in solutionPath:
            print(p)

    #Heuristics being used
    heuristic = ['misplaced', 'manhattan', 'euclidean']

    #Initial board states
    initialStates = ["3,6,5,2,1,4,7,8,0", "1,3,2,6,7,5,4,8,0"]

    #For each heuristic
    for h in heuristic:
        #Lists to store the steps for average computation
        bfsSteps = []
        astarSteps = []
        for start in initialStates:
            s = Board(start)

            #BFS with chosen heuristic
            print("=" * 25 + "BFS with " + h.capitalize() + "=" * 25)
            print(s)
            bfsStates, bfsSol = bfs(start, h)
            if bfsStates <= MAX_MOVES:
                bfsPath = bfsSol.traversePath([])
                printSolution(bfsPath)
                bfsSteps.append(len(bfsPath))
                print("Solved in " + str(len(bfsPath)) + " steps")
                print("Explored " + str(bfsStates) + " states")
            else:
                print("Reached maximum number of moves of " + str(MAX_MOVES))

            print("=" * 68 + "\n")

            #A* with chosen heuristic
            print("=" * 25 + "A* with " + h.capitalize() + "=" * 25)
            print(s)
            astarStates, astarSol = astar(start, h)
            if astarStates <= MAX_MOVES:
                astarPath = astarSol.traversePath([])
                printSolution(astarPath)
                astarSteps.append(len(astarPath))
                print("Solved in " + str(len(astarPath)) + " steps")
                print("Explored " + str(astarStates) + " states")
            else:
                print("Reached maximum number of moves of " + str(MAX_MOVES))
            print("=" * 67 + "\n")
        
        #Print averages
        print("=" * 20 + h.capitalize() + " Summary" + "=" * 20)
        print("Average number of steps with BFS: " + str(np.average(bfsSteps)))
        print("Average number of steps with A*: " + str(np.average(astarSteps)))
        print("=" * 67 + "\n")

if __name__ == '__main__':
    main()
