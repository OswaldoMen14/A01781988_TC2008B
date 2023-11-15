from mesa import Agent
from random import choice
from queue import PriorityQueue

class ChargingStation(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.is_charging = False

    def charging_status(self):
        return self.is_charging

class Roomba(Agent):
    def __init__(self, unique_id, model, charging_station_pos):
        super().__init__(unique_id, model)
        self.charging_station_pos = charging_station_pos
        self.steps_taken = 0
        self.battery_level = 100
        self.is_charging = False
        self.charge_cooldown = 0
        self.last_pos = None
        self.battery_threshold = 10
        self.direction = 'right'
        self.avoiding_obstacle = False
        self.visited_positions = set()

    def is_path_clear(self, pos):
        x, y = pos
        grid_width, grid_height = self.model.grid.width, self.model.grid.height
        return 0 <= x < grid_width and 0 <= y < grid_height and all(not isinstance(agent, ObstacleAgent) for agent in self.model.grid.get_cell_list_contents(pos))

    def move(self):
        x, y = self.pos
        possible_moves = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
        new_moves = [move for move in possible_moves if move not in self.visited_positions and self.is_path_clear(move)]
        new_pos = choice(new_moves) if new_moves else choice([move for move in possible_moves if self.is_path_clear(move)])
        if new_pos != self.pos:
            self.model.grid.move_agent(self, new_pos)
            self.clean_trash()
            self.visited_positions.add(new_pos)

    def clean_trash(self):
        cell_contents = self.model.grid.get_cell_list_contents([self.pos])
        trash_agents = [agent for agent in cell_contents if isinstance(agent, TrashAgent)]
        for agent in trash_agents:
            self.model.grid.remove_agent(agent)
            self.model.schedule.remove(agent)

    def navigate_to_charging_station(self):
        current_x, current_y = self.pos
        station_x, station_y = self.charging_station_pos

        # Implementing Dijkstra's algorithm to find the shortest path
        visited = set()
        distances = {(x, y): float('inf') for x in range(self.model.grid.width) for y in range(self.model.grid.height)}
        distances[self.pos] = 0
        priority_queue = PriorityQueue()
        priority_queue.put((0, self.pos))

        while not priority_queue.empty():
            current_distance, current_pos = priority_queue.get()

            if current_pos in visited:
                continue

            visited.add(current_pos)

            if current_pos == self.charging_station_pos:
                break

            x, y = current_pos
            neighbors = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
            valid_neighbors = [neighbor for neighbor in neighbors if self.is_path_clear(neighbor)]

            for neighbor in valid_neighbors:
                new_distance = distances[current_pos] + 1  # Assuming each step has a cost of 1
                if new_distance < distances[neighbor]:
                    distances[neighbor] = new_distance
                    priority_queue.put((new_distance, neighbor))

        # Reconstructing the path
        path = [self.charging_station_pos]
        current_pos = self.charging_station_pos
        while current_pos != self.pos:
            x, y = current_pos
            neighbors = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
            valid_neighbors = [neighbor for neighbor in neighbors if self.is_path_clear(neighbor)]
            next_pos = min(valid_neighbors, key=lambda pos: distances[pos])
            path.insert(0, next_pos)
            current_pos = next_pos

        # Moving to the next position in the path
        next_pos = path[1]
        self.model.grid.move_agent(self, next_pos)

    def step(self):
        if self.pos == self.charging_station_pos:
            charging_station = self.get_charging_station()
            if self.battery_level < 100:
                self.battery_level += 5
                charging_station.is_charging = True
            else:
                charging_station.is_charging = False
                if self.charge_cooldown == 0:
                    self.move()
        else:
            if self.battery_level <= self.battery_threshold and not self.is_charging:
                self.navigate_to_charging_station()
            elif self.battery_level > self.battery_threshold:
                self.move()
                self.battery_level -= 1

    def get_charging_station(self):
        return next((agent for agent in self.model.schedule.agents if isinstance(agent, ChargingStation)), None)

class ObstacleAgent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        pass

class TrashAgent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.steps_taken = 0
