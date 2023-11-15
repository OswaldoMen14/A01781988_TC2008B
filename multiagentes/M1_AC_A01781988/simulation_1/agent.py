from mesa import Agent

status_rules = {("Dead", "Dead", "Dead"):"Dead",
                        ("Dead","Dead","Alive"):"Alive",
                        ("Dead","Alive","Dead"):"Dead",
                        ("Dead","Alive","Alive"):"Alive",
                        ("Alive","Dead","Dead"):"Alive",
                        ("Alive","Dead","Alive"):"Dead",
                        ("Alive","Alive","Dead"):"Alive",
                        ("Alive","Alive","Alive"):"Dead"
                        }

class AutomataCelular(Agent):
    """
        Un automata celular:         
        Atributos:
            x, y: Grid coordinates
            condition: Can be "Alive" or "Dead". 
            unique_id: (x,y) tuple.

            unique_id isn't strictly necessary here, but it's good practice to give one to each agent anyway.
    """

    def __init__(self, pos, model):
        """
        Create a new cell. 

        Args:
            pos: The cell's coordinates on the grid.
            model: standard model reference for agent.
        """
        super().__init__(pos, model)
        self.pos = pos
        self.condition = "Dead"
        self._next_condition = None

    def step(self):
        """
        En base a los 3 vecinos de arriba de cada agente, 
        actualiza el estado del agente siguiendo las siguientes reglas, 
        donde 0 significa Dead, y 1 significa Alive
        """
        neighbor_states = [neighbor.condition for neighbor in self.model.grid.iter_neighbors(self.pos, True) if neighbor.pos[1] > self.pos[1]]
        self._next_condition = status_rules.get(tuple(neighbor_states))
        
    def advance(self):
        """
        Advance the model by one step.
        """
        if self._next_condition is not None:
            self.condition = self._next_condition