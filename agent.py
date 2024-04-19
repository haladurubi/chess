from envs.game import State
from agent_interface import AgentInterface
import chess



class Agent(AgentInterface):
    """
    An agent who plays Chess

    Methods
    -------
    `info` returns the agent's information
    `decide` chooses an action from possible actions
    """
    def __init__(self, depth: int = 4):
        self.depth = depth
        self.__player = None

    def heuristic(self, state: State,deciding_agent : int):
        if deciding_agent == 0:
            COLOR = chess.WHITE
            otherCOLOR = chess.BLACK
        else:
            COLOR = chess.BLACK
            otherCOLOR = chess.WHITE

        knights = state.board.pieces(chess.KNIGHT,COLOR)
        bishops = state.board.pieces(chess.BISHOP,COLOR)
        queens = state.board.pieces(chess.QUEEN,COLOR)

        Oknights = state.board.pieces(chess.KNIGHT,otherCOLOR)
        Obishops = state.board.pieces(chess.BISHOP,otherCOLOR)
        Oqueens = state.board.pieces(chess.QUEEN,otherCOLOR)

        score = 3 * len(knights) + 3 * len(bishops) + 7 * len(queens) - 2 * len(Oknights) - 2 * len(Obishops) - 5 * len(Oqueens)

        return score


    @staticmethod
    def info():
        """
        Return the agent's information

        Returns
        -------
        Dict[str, str]
            `agent name` is the agent's name
            `student name` is the list team members' names
            `student number` is the list of student numbers of the team members
        """
        # -------- Task 1 -------------------------
        # Please complete the following information
        # NOTE: Please try to pick a unique name for you agent. If there are
        #       some duplicate names, we have to change them.

        return {"agent name": "lalapheta",  # COMPLETE HERE
                "student name": ["Hala Durubi"],  # COMPLETE HERE
                "student number": ["100958845"]}  # COMPLETE HERE


    def decide(self, state: State):
        """
        Generate a sequence of increasingly preferable actions

        Given the current `state`, this function should choose the action that
        leads to the agent's victory.
        However, since there is a time limit for the execution of this function,
        it is possible to choose a sequence of increasing preferable actions.
        Therefore, this function is designed as a generator; it means it should
        have no return statement, but it should `yield` a sequence of increasing
        good actions.

        IMPORTANT: If no action is yielded within the time limit, the game will
        choose a random action for the player.

        NOTE: You can find the possible actions and next states by using
              the `successors()` method of the `state`. In other words,
              `state.successors()` return a list of pairs of `action` and its
              corresponding next state.

        Parameters
        ----------
        state: State
            Current state of the game

        Yields
        ------
        action
            the chosen `action`
        """

        # -------- TASK 2 ------------------------------------------------------
        # Your task is to implement an algorithm to choose an action form the
        # possible `actions` in the `state.successors()`. You can implement any
        # algorithm you want.
        # However, you should keep in mind that the execution time of this
        # function is limited. So, instead of choosing just one action, you can
        # generate a sequence of increasingly good action.
        # This function is a generator. So, you should use `yield` statement
        # rather than `return` statement. To find more information about
        # generator functions, you can take a look at:
        # https://www.geeksforgeeks.org/generators-in-python/
        #
        # If you generate multiple actions, the last action will be used in the
        # game.
        #
        #
        # Tips
        # ====
        # 0. You can improve the `MinimaxAgent` to implement the Alpha-beta
        #    pruning approach.
        #    Also, By using `IterativeDeepening` class you can simply add
        #    the iterative deepening feature to your Alpha-beta agent.
        #    You can find an example of this in `id_minimax_agent.py` file.
        # 
        # 1. You can improve the heuristic function of `MinimaxAgent`.
        #
        # 2. If you need to simulate a game from a specific state to find the
        #    the winner, you can use the following pattern:
        #    ```
        #    simulator = Game(FirstAgent(), SecondAgent())
        #    winner = simulator.play(starting_state=specified_state)
        #    ```
        #    The `MCSAgent` has illustrated a concrete example of this
        #    pattern.
        #
        #
        #
        # GL HF :)
        # ----------------------------------------------------------------------

        # Replace the following lines with your algorithm
        
        def alphabeta(state: State, depth, alpha, beta, deciding):
            if depth == 0 or state.is_winner():
                return self.heuristic(state, deciding), None
            
            best_action = None
            if state.current_player() == deciding: 
                value = float('-inf')
                for action in state.applicable_moves():
                    next_state = state.clone()
                    next_state.execute_move(action)
                    next_value, _ = alphabeta(next_state, depth - 1, alpha, beta, deciding)
                    if next_value > value:
                        value = next_value
                        best_action = action
                    alpha = max(alpha, value)
                    if alpha >= beta:
                        break
                return value, best_action
            else: 
                value = float('inf')
                for action in state.applicable_moves():
                    next_state = state.clone()
                    next_state.execute_move(action)
                    next_value, _ = alphabeta(next_state, depth - 1, alpha, beta, deciding)
                    if next_value < value:
                        value = next_value
                        best_action = action
                    beta = min(beta, value)
                    if alpha >= beta:
                        break
                return value, best_action

        # Initial values for alpha and beta
        alpha = float('-inf')
        beta = float('inf')

        # Call alphabeta function to get the best action
        _, best_action = alphabeta(state.clone(), self.depth, alpha, beta, state.current_player())

        # Yield the best action
        yield best_action