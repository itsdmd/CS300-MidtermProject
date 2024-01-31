# Solver for sokuban game using following search strategies:
# - Breadth-first search
# - Depth-first search
# - A* search
# - Uniform-cost search
# - Greedy search
# - Custom strategy
# The solver class has the following methods:
# - solve(): solve the game
# """

import time
from collections import deque
from queue import Queue

from modules.game_state import GameState


class Solver(object):
    def __init__(self, initial_state, strategy):
        self.initial_state = initial_state
        self.strategy = strategy
        self.solution = None
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
        visited = set()
        queue = deque([(self.initial_state, [])])

        while queue:
            state, path = queue.popleft()

            if state.check_solved():
                return path

            visited.add(state)

            for neighbor in state.generate_neighbors():
                if neighbor not in visited:
                    queue.append((neighbor, path + [neighbor]))
        return None

    def dfs(self):
        visited = set()
        stack = [(self.initial_state, [])]

        while stack:
            state, path = stack.pop()

            if state.check_solved():
                return path

            visited.add(state)

            for neighbor in state.generate_neighbors():
                if neighbor not in visited:
                    stack.insert(0, (neighbor, path + [neighbor]))

        return None

    def astar(self):
        pass

    def ucs(self):
        pass

    def greedy(self):
        pass

    def custom(self):
        return [
            "U",
            "U",
        ]

    def get_solution(self):
        return self.solution
