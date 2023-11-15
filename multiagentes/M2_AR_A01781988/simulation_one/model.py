from mesa import Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa import DataCollector
from agent import Roomba, ObstacleAgent, TrashAgent, ChargingStation

class CleaningModel(Model):
    """ 
    Creates a new model with random agents.
    Args:
        N: Number of agents in the simulation
        height, width: The size of the grid to model
    """

    def __init__(self, N, width, height, amount_trash):
        self.current_id = 0
        self.num_agents = N
        # Multigrid is a special type of grid where each cell can contain multiple agents.
        self.grid = MultiGrid(width, height, torus=False)

        # RandomActivation is a scheduler that activates each agent once per step, in random order.
        self.schedule = RandomActivation(self)

        self.running = True 

        # Initialize a single Roomba and its ChargingStation at (1, 1)
        charging_station_pos = (1, 1)
        charging_station = ChargingStation(self.next_id(), self)
        self.grid.place_agent(charging_station, charging_station_pos)
        self.schedule.add(charging_station)  # Don't forget to add to the schedule!

        roomba = Roomba(self.next_id(), self, charging_station_pos)
        self.grid.place_agent(roomba, charging_station_pos)
        self.schedule.add(roomba)

        self.datacollector = DataCollector( 
        agent_reporters={"Steps": lambda a: a.steps_taken if isinstance(a, Roomba) else 0}) # métrica de desempeño: cuanta basura queda, cuanta se levanta y que tan rápido se levanta

        # Creates the border of the grid
        border = [(x, y) for y in range(height) for x in range(width) if y in [0, height-1] or x in [0, width - 1]]  # lista de posiciones de los bordes
        # en el if checas que tu coordenada en x o en y esté en el borde, genera una lista de tuplas

        # Add obstacles to the grid, agrega agentes
        for pos in border:
            obs = ObstacleAgent(pos, self)
            self.grid.place_agent(obs, pos)
        
        # Function to generate random positions
        pos_gen = lambda w, h: (self.random.randrange(w), self.random.randrange(h))  # función lambda que genera posiciones aleatorias

        # Add the agent to a random empty grid cell
        for i in range(self.num_agents): 
            o = ObstacleAgent(i + 3000, self)  # el primer parámetro es un id único para cada agente, el segundo es el modelo
            # también hay que asignar un id a los obstáculos, paredes, etc. 
            self.schedule.add(o)

            # utiliza la función lambda para generar posiciones aleatorias
            pos = pos_gen(self.grid.width, self.grid.height)

            # revisa si la posición está vacía, si no lo está, genera otra posición
            while not self.grid.is_cell_empty(pos):
                pos = pos_gen(self.grid.width, self.grid.height)
            # si la posición está vacía, coloca al agente en esa posición
            self.grid.place_agent(o, pos)
        
        self.datacollector.collect(self)

        # Add the trash agent to a random empty grid cell
        for i in range(amount_trash): 
            t = TrashAgent(i + 2000, self)  # el primer parámetro es un id único para cada agente, el segundo es el modelo
            # también hay que asignar un id a los obstáculos, paredes, etc. 
            self.schedule.add(t)

            # utiliza la función lambda para generar posiciones aleatorias
            pos = pos_gen(self.grid.width, self.grid.height)

            # revisa si la posición está vacía, si no lo está, genera otra posición
            while not self.grid.is_cell_empty(pos):
                pos = pos_gen(self.grid.width, self.grid.height)
            # si la posición está vacía, coloca al agente en esa posición
            self.grid.place_agent(t, pos)
        
        self.datacollector.collect(self)

    def next_id(self):
        self.current_id += 1
        return self.current_id

    def step(self):
        '''Advance the model by one step.'''
        # self.schedule.step() llama al método step de cada agente
        self.schedule.step()
        self.datacollector.collect(self)
