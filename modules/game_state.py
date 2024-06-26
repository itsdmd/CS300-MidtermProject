"""
Sokuban game state class
The state of the game consists the map which is a 2D array of characters. There are 6 types of characters:
- ' ': empty space
- '#': wall
- '$': box
- '.': target
- '@': player
- '+': player on target
- '*': box on target
The game state class keeps track of the map.
The game state also keeps track of the player and box positions, and whether the game is solved or not.
The game state class has the following methods:
- find_player(): find the player in the map and return its position
- find_boxes(): find all the boxes in the map and return their positions
- find_targets(): find all the targets in the map and return their positions
- find_targets_without_box(): find all the targets without a box on top in the map and return their positions

- is_wall(position): check if the given position is a wall
- is_box(position): check if the given position is a box
- is_target(position): check if the given position is a target
- is_empty(position): check if the given position is empty

- get_distance(position1, position2): get the distance between two positions using Manhattan distance
- get_nearest_target(position): get the nearest target from the given position by exhaustive iteration
- get_heuristic(): get the heuristic for the game state
- get_total_cost(): get the sum of the current cost and the heuristic
- get_current_cost(): get the current cost for the game state

- new_position(position, direction): get the new position after moving to the given direction
- is_stuck(box): check if a given box cannot be moved
- has_stuck_box(): check if the game state has a stuck box

- move(direction): generate the next game state by moving the player to the given direction

- generate_neighbors(): generate the neighbors/successors of the game state by moving the player in all directions
- check_solved(): check if the game is solved
- print_state(): print the game state
"""

from copy import deepcopy


class GameState:
    def __init__(self, map, current_cost=0):
        self.set_state(map, current_cost)

    def set_state(self, map, current_cost=0):
        self.map = map
        self.current_cost = current_cost
        self.height = len(self.map)
        self.width = len(self.map[0])
        self.player = self.find_player()
        self.boxes = self.find_boxes()
        self.targets = self.find_targets()
        self.targets_without_box = self.find_targets_without_box()
        self.is_solved = self.check_solved()
        self.compare_value = 0
        self.last_move = "N"

    def __lt__(self, other):
        return self.compare_value < other.compare_value

    # ------------------------------------------------------------------------------------------------------------------
    # The following methods are used to find the player, boxes, and targets in the map
    # The positions are tuples (row, column)
    # ------------------------------------------------------------------------------------------------------------------

    def find_player(self):
        """Find the player in the map and return its position"""
        for y, row in enumerate(self.map):
            for x, cell in enumerate(row):
                if cell in ("@", "+"):  # Player or player on target
                    return y, x
        return None

    def find_boxes(self):
        """Find all the boxes in the map and return their positions"""
        boxes = []
        for y, row in enumerate(self.map):
            for x, cell in enumerate(row):
                if self.is_box((y, x)):  # Box or box on target
                    boxes.append((y, x))
        return boxes

    def find_targets(self):
        """Find all the targets in the map and return their positions"""
        """Find all the boxes in the map and return their positions"""
        targets = []
        for y, row in enumerate(self.map):
            for x, cell in enumerate(row):
                if self.is_target((y, x)):  # Target or box on target
                    targets.append((y, x))
        return targets

    def find_targets_without_box(self):
        """Find all the targets without a box on top in the map and return their positions"""
        targets = []
        for y, row in enumerate(self.map):
            for x, cell in enumerate(row):
                if self.is_target((y, x)) and not self.is_box((y, x)):
                    targets.append((y, x))
        return targets

    # ------------------------------------------------------------------------------------------------------------------
    # The following methods are used to check if a position is a wall, box, target, or empty space
    # The position is a tuple (row, column)
    # ------------------------------------------------------------------------------------------------------------------

    def is_wall(self, position):
        """Check if the given position is a wall"""
        x, y = position
        if self.map[x][y] == "#":
            return True
        return False

    def is_box(self, position):
        """Check if the given position is a box
        Note: the box can be on "$" or "*" (box on target)
        """
        x, y = position
        if self.map[x][y] in ("$", "*"):
            return True
        return False

    def is_target(self, position):
        """Check if the given position is a target
        Note: the target can be "." or "*" (box on target)
        """
        x, y = position
        if self.map[x][y] in (".", "*"):
            return True
        return False

    def is_empty(self, position):
        """Check if the given position is empty"""
        x, y = position
        if self.map[x][y] == " ":
            return True
        return False

    # ------------------------------------------------------------------------------------------------------------------
    # The following methods get heuristics for the game state (for informed search strategies)
    # ------------------------------------------------------------------------------------------------------------------

    def get_distance(self, position1, position2):
        """Get the distance between two positions using Manhattan distance"""
        return abs(position1[0] - position2[0]) + abs(position1[1] - position2[1])

    def get_nearest_target(self, position):
        """Get the nearest target from the given position by exhaustive iteration"""
        nearest_target = None
        nearest_distance = self.height + self.width

        for target in self.targets:
            distance = self.get_distance(position, target)
            if distance < nearest_distance:
                nearest_target = target
                nearest_distance = distance

        return nearest_target

    def get_heuristic(self):
        heuristic_value = 0
        for box in self.boxes:
            distances = [
                # Get all distances from this box to all targets without a box on top
                self.get_distance(box, target)
                for target in self.targets_without_box
            ]
            if distances:
                # Add the minimum distance to the heuristic value
                heuristic_value += min(distances)

        return heuristic_value

    def get_total_cost(self):
        """Get the cost for the game state
        Note: the cost is the number of moves from the initial state to the current state + the heuristic
        """
        return self.current_cost + self.get_heuristic()

    def get_current_cost(self):
        """Get the current cost for the game state
        Note: the current cost is the number of moves from the initial state to the current state
        """
        return self.current_cost

    # ------------------------------------------------------------------------------------------------------------------
    # The following methods are used to generate the next game state and check if the game is solved
    # ------------------------------------------------------------------------------------------------------------------

    def new_position(self, position, direction):
        """Get the new position after moving to the given direction"""
        # Check if out of bound
        if (
            position[0] < 0
            or position[0] >= self.height
            or position[1] < 0
            or position[1] >= self.width
        ):
            return position
        if direction == "U":
            return (position[0] - 1, position[1])
        elif direction == "D":
            return (position[0] + 1, position[1])
        elif direction == "L":
            return (position[0], position[1] - 1)
        elif direction == "R":
            return (position[0], position[1] + 1)
        elif direction == "N":
            return position
        else:
            raise Exception("Invalid direction")

    def is_stuck(self, box):
        """Check if a given box cannot be moved
        by checking whether it is adjacent to 2 diagonally opposite walls
        """
        # Make sure the box is not on target
        if self.map[box[0]][box[1]] == "$":
            # Get adjacent horizontal and vertical cells coordinates
            adjacent_cells = [
                (box[0] - 1, box[1]),  # Left
                (box[0] + 1, box[1]),  # Right
                (box[0], box[1] - 1),  # Up
                (box[0], box[1] + 1),  # Down
            ]
            # Check if the box is adjacent to 2 diagonally opposite walls
            # Iterate through all horizontal and vertical adjacent cells
            for i in range(len(adjacent_cells)):
                # For each adjacent cell, check if there is another adjacent cell that is diagonally opposite
                for j in range(i + 1, len(adjacent_cells)):
                    # The cell is diagonally opposite if the row and column differences are both 2
                    if (
                        self.is_wall(adjacent_cells[i])
                        and self.is_wall(adjacent_cells[j])
                        and (
                            (i == 0 and j == 2)  # Left and Up
                            or (i == 0 and j == 3)  # Left and Down
                            or (i == 1 and j == 2)  # Right and Down
                            or (i == 1 and j == 3)  # Right and Up
                        )
                    ):
                        return True
        return False

    def has_stuck_box(self):
        """Check if the game state has a deadlock box
        (a box that cannot be pushed to a target because it is in a deadlock position)
        """
        for box in self.boxes:
            if self.is_stuck(box):
                return True
        return False

    def move(self, direction):
        """Generate the next game state by moving the player to the given direction.
        The rules are as follows:
        - The player can move to an empty space
        - The player can move to a target
        - The player can push a box to an empty space (the box moves to the empty space, the player moves to the box's previous position)
        - The player can push a box to a target (the box moves to the target, the player moves to the box's previous position)
        - The player cannot move to a wall
        - The player cannot push a box to a wall
        - The player cannot push two boxes at the same time
        """
        self.last_move = direction
        new_pos = self.new_position(self.player, direction)

        if self.is_empty(new_pos):
            # Check if player is on target
            if self.map[self.player[0]][self.player[1]] == "+":
                self.map[self.player[0]][self.player[1]] = "."
            else:
                self.map[self.player[0]][self.player[1]] = " "
            self.map[new_pos[0]][new_pos[1]] = "@"
            self.player = new_pos

            self.current_cost += 1
            return self

        # Check if player is on target and not on box-on-target
        if self.is_target(new_pos) and not self.is_box(new_pos):
            if self.map[self.player[0]][self.player[1]] == "+":
                self.map[self.player[0]][self.player[1]] = "."
            else:
                self.map[self.player[0]][self.player[1]] = " "
            self.map[new_pos[0]][new_pos[1]] = "+"
            self.player = new_pos

            self.current_cost += 1
            return self

        if self.is_wall(new_pos):
            self.current_cost += 1
            return self

        if self.is_box(new_pos):
            new_box_pos = self.new_position(
                new_pos, direction
            )  # Position where the box is pushed to

            # If the box is pushed to an empty space
            if self.is_empty(new_box_pos):
                # If box currently on target, set current position to target
                if self.map[new_pos[0]][new_pos[1]] == "*":
                    self.map[new_pos[0]][new_pos[1]] = "."
                else:
                    self.map[new_pos[0]][new_pos[1]] = " "
                # Update the box position
                self.map[new_box_pos[0]][new_box_pos[1]] = "$"
                self.boxes.remove(new_pos)
                self.boxes.append(new_box_pos)

                # If player currently on target, set current position to target
                if self.map[self.player[0]][self.player[1]] == "+":
                    self.map[self.player[0]][self.player[1]] = "."
                else:
                    self.map[self.player[0]][self.player[1]] = " "
                # Update the player position
                # If position where box was pushed from is target, set player position to be on target
                if self.map[new_pos[0]][new_pos[1]] == ".":
                    self.map[new_pos[0]][new_pos[1]] = "+"
                else:
                    self.map[new_pos[0]][new_pos[1]] = "@"
                self.player = new_pos

                self.current_cost += 1
                return self

            # If the box is pushed to a target
            if self.is_target(new_box_pos) and not self.is_box(new_box_pos):
                # Update the box position
                if self.map[new_pos[0]][new_pos[1]] == "*":
                    self.map[new_pos[0]][new_pos[1]] = "."
                else:
                    self.map[new_pos[0]][new_pos[1]] = " "
                self.map[new_box_pos[0]][new_box_pos[1]] = "*"
                self.boxes.remove(new_pos)
                self.boxes.append(new_box_pos)

                # Update the player position
                if self.map[self.player[0]][self.player[1]] == "+":
                    self.map[self.player[0]][self.player[1]] = "."
                else:
                    self.map[self.player[0]][self.player[1]] = " "
                if self.map[new_pos[0]][new_pos[1]] == ".":
                    self.map[new_pos[0]][new_pos[1]] = "+"
                else:
                    self.map[new_pos[0]][new_pos[1]] = "@"
                self.player = new_pos

                self.current_cost += 1
                return self

            # If the box is pushed to a wall
            if self.is_wall(new_box_pos):
                self.current_cost += 1
                return self

            # If the box is pushed to another box
            if self.is_box(new_box_pos):
                self.current_cost += 1
                return self

        return self

    def generate_neighbors(self):
        """Generate the neighbors of the game state by moving the player in all directions"""
        neighbors = []
        for direction in ["U", "D", "L", "R"]:
            neighbor = deepcopy(self)
            neighbor.move(direction)
            # neighbor.print_state()

            # If generated neighbor does not have a deadlock box and is not have the same map as the current state
            if not neighbor.has_stuck_box() and str(neighbor.map) != str(self.map):
                if neighbor.check_solved():
                    return [neighbor]
                else:
                    neighbors.append(neighbor)
        return neighbors

    def check_solved(self):
        """Check if the game is solved"""
        for target in self.targets:
            if self.map[target[0]][target[1]] != "*":
                return False
        return True

    def print_state(self):
        """Print the game state"""
        print(
            "Heuristic: "
            + str(self.get_heuristic())
            + " | "
            + " Cost: "
            + str(self.get_current_cost())
        )
        for row in self.map:
            print("".join(row))
        print("")
