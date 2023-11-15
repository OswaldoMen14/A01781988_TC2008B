from mesa import Agent
# Define the status rules for each cell 
status_rules = {
    ("Dead", "Dead", "Dead"): "Dead",
    ("Dead", "Dead", "Alive"): "Alive",
    ("Dead", "Alive", "Dead"): "Dead",
    ("Dead", "Alive", "Alive"): "Alive",
    ("Alive", "Dead", "Dead"): "Alive",
    ("Alive", "Dead", "Alive"): "Dead",
    ("Alive", "Alive", "Dead"): "Alive",
    ("Alive", "Alive", "Alive"): "Dead"
}

class AutomataCelular(Agent):
    def __init__(self, pos, model):
        super().__init__(pos, model)
        self.pos = pos
        self.condition = "Dead"
        self._next_condition = None

    def step(self):
         # Initialize a list to store the states of neighbors
        neighborStates = ["Dead"] * 3

        # Check if the agent is at the top row
        if self.pos[1] == 49:
            left = self.model.grid[self.pos[0] - 1, 0]
            right = self.model.grid[self.pos[0] + 1, 0]
        else:
            left = self.model.grid[self.pos[0] - 1, self.pos[1] + 1]
            right = self.model.grid[self.pos[0] + 1, self.pos[1] + 1]

        central = self.model.grid[self.pos[0], self.pos[1] + 1]

        # Populate the neighborStates list with the conditions of the neighbors
        neighborStates[0] = left.condition
        neighborStates[1] = central.condition
        neighborStates[2] = right.condition

        current_state = tuple(neighborStates)
        # Use the status_rules dictionary to determine the next state
        self._next_condition = status_rules[current_state]

    def advance(self):
        if self._next_condition is not None:
            self.condition = self._next_condition
