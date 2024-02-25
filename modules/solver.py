import time
from collections import deque
from queue import Queue, PriorityQueue

from modules.game_state import GameState


class Solver(object):
    def __init__(self, initial_state, strategy):
        self.initial_state = initial_state
        self.strategy = strategy
        self.solution = None
        self.num_of_expanded = 0
        self.num_of_generated = 0
        self.time = None

    def solve(self):
        start_time = time.time()
        if self.strategy == "bfs":
            self.solution = self.bfs()
        elif self.strategy == "dfs":
            self.solution = self.dfs()
        elif self.strategy == "astar":
            self.solution = self.astar()
        elif self.strategy == "ucs":
            self.solution = self.ucs()
        elif self.strategy == "greedy":
            self.solution = self.greedy()
        elif self.strategy == "custom":
            self.solution = self.custom()
        else:
            raise Exception("Invalid strategy")
        self.time = time.time() - start_time

    def bfs(self):
        visited = set()  # Set to keep track of visited nodes
        queue = deque(
            [(self.initial_state, [])]
        )  # Queue to keep track of states to explore. Initialize with the initial state.

        # While there are states to explore
        while queue:
            # Get the next state to explore
            state, path = queue.popleft()  # Pop the leftmost state from the queue.
            self.num_of_expanded += 1

            # If the state is solved, return the path
            if state.check_solved():
                return path

            # Add the state to the visited set
            visited.add(str(state.map))

            # Get list of neighbors of the state
            neighbors = state.generate_neighbors()
            self.num_of_generated += len(neighbors)

            # Iterate through the neighbors
            for n in neighbors:
                if n.check_solved():
                    return path + [n.last_move]
                # If the neighbor has not been visited, add it to the back of the queue.
                if str(n.map) not in visited:
                    visited.add(str(n.map))
                    queue.append((n, path + [n.last_move]))

        return None

    def dfs(self):
        visited = set()

        def dfs_recursive(state, path, visited):
            if state.check_solved():
                return path

            visited.add(str(state.map))

            neighbors = state.generate_neighbors()
            self.num_of_generated += len(neighbors)

            for n in neighbors:
                if n.check_solved():
                    return path + [n.last_move]
                if str(n.map) not in visited:
                    self.num_of_expanded += 1
                    visited.add(str(n.map))
                    result = dfs_recursive(n, path + [n.last_move], visited)
                    if result:
                        return result

            return None

        return dfs_recursive(self.initial_state, [], visited)

    def ucs(self):
        visited = set()
        priority_queue = PriorityQueue()
        priority_queue.put((0, self.initial_state, []))

        while not priority_queue.empty():
            (
                cost,
                state,
                path,
            ) = priority_queue.get()  # UCS uses the cost for prioritizing the states

            self.num_of_expanded += 1

            if state.check_solved():
                return path

            visited.add(str(state.map))

            neighbors = state.generate_neighbors()
            self.num_of_generated += len(neighbors)

            for n in neighbors:
                if n.check_solved():
                    return path + [n.last_move]
                if str(n.map) not in visited:
                    visited.add(str(n.map))
                    n.compare_value = cost + 1
                    priority_queue.put((n.compare_value, n, path + [n.last_move]))

        return None

    def astar(self):
        visited = set()
        priority_queue = (
            PriorityQueue()
        )  # Priority queue is used for automatic sorting of the states based on their compare_value
        priority_queue.put((0, self.initial_state, []))

        while not priority_queue.empty():
            (
                _,
                state,
                path,
            ) = (
                priority_queue.get()
            )  # Astar uses the compare_value for prioritizing the states

            self.num_of_expanded += 1

            if state.check_solved():
                return path

            visited.add(str(state.map))

            neighbors = state.generate_neighbors()
            self.num_of_generated += len(neighbors)

            for n in neighbors:
                if n.check_solved():
                    return path + [n.last_move]
                if str(n.map) not in visited:
                    visited.add(str(n.map))
                    # Compare value is the total cost of the state
                    n.compare_value = n.get_total_cost()
                    # The object with format (compare_value, state, path) is added to the priority queue
                    priority_queue.put((n.compare_value, n, path + [n.last_move]))

        return None

    def greedy(self):
        visited = set()
        priority_queue = PriorityQueue()
        priority_queue.put((0, self.initial_state, []))

        while not priority_queue.empty():
            (
                _,
                state,
                path,
            ) = (
                priority_queue.get()
            )  # Greedy search uses the heuristic value for prioritizing the states

            self.num_of_expanded += 1

            if state.check_solved():
                return path

            visited.add(str(state.map))

            neighbors = state.generate_neighbors()
            self.num_of_generated += len(neighbors)

            for n in neighbors:
                if n.check_solved():
                    return path + [n.last_move]
                if str(n.map) not in visited:
                    visited.add(str(n.map))
                    n.compare_value = n.get_heuristic()
                    priority_queue.put((n.compare_value, n, path + [n.last_move]))

        return None

    def custom(self):
        return [
            "U",
            "D",
            "L",
            "R",
        ]

    def get_solution(self):
        return self.solution

    def print_solution(self):
        print("Solution: " + str(self.solution))

    def print_num_of_expanded(self):
        print("Number of states expanded: " + str(self.num_of_expanded))

    def print_num_of_generated(self):
        print("Number of states generated: " + str(self.num_of_generated))

    def print_number_of_moves(self):
        print("Number of moves: " + str(len(self.solution)))

    def print_time(self):
        print("Time taken: " + str(self.time))
