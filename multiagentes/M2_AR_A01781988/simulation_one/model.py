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

    def __init__(self, N, width, height, amount_trash, num_obstacles):
        self.current_id = 0
        self.num_agents = N
        self.total_time = 0
        self.clean_percentage = 0
        # Multigrid is a special type of grid where each cell can contain multiple agents.
        self.grid = MultiGrid(width, height, torus=False)

        # RandomActivation is a scheduler that activates each agent once per step, in random order.
        self.schedule = RandomActivation(self)
        self.running = True 

        # Initialize a single Roomba and its ChargingStation at (1, 1)
        charging_station_pos = (1, 1)
        charging_station = ChargingStation(self.next_id(), self)
        self.grid.place_agent(charging_station, charging_station_pos)
        self.schedule.add(charging_station)

        roomba = Roomba(self.next_id(), self, charging_station_pos)
        self.grid.place_agent(roomba, charging_station_pos)
        self.schedule.add(roomba)

        self.datacollector = DataCollector( 
        agent_reporters={"Steps": lambda a: a.steps_taken if isinstance(a, Roomba) else 0,
                        "Cleaning percentage": lambda m: m.cleaning_percentage if isinstance(m, Roomba) else 0},
        model_reporters={"Total Time": "total_time"}) 

        # Creates the border of the grid
        border = [(x, y) for y in range(height) for x in range(width) if y in [0, height-1] or x in [0, width - 1]]  

        for pos in border:
            obs = ObstacleAgent(pos, self)
            self.grid.place_agent(obs, pos)
        
        pos_gen = lambda w, h: (self.random.randrange(w), self.random.randrange(h)) 

        for i in range(num_obstacles):
            o = ObstacleAgent(self.next_id(), self)
            pos = pos_gen(self.grid.width, self.grid.height)
            while not self.grid.is_cell_empty(pos):
                pos = pos_gen(self.grid.width, self.grid.height)
            self.grid.place_agent(o, pos)
            self.schedule.add(o) 

        
        self.datacollector.collect(self)

        for i in range(amount_trash): 
            t = TrashAgent(i + 2000, self)  
            self.schedule.add(t)

            pos = pos_gen(self.grid.width, self.grid.height)

            while not self.grid.is_cell_empty(pos):
                pos = pos_gen(self.grid.width, self.grid.height)
            self.grid.place_agent(t, pos)
        
        self.datacollector.collect(self)

    def next_id(self):
        self.current_id += 1
        return self.current_id

    def step(self):
        '''Advance the model by one step.'''
        trash_agents_exist = any(isinstance(agent, TrashAgent) for agent in self.schedule.agents)

        if not trash_agents_exist:
            self.running = False
            return
        
        self.schedule.step()
        self.datacollector.collect(self)

        if self.schedule.steps == 149:
            self.running = False
        
        self.total_time += 1

        