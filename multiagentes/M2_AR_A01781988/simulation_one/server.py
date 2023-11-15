from model import CleaningModel, ObstacleAgent, TrashAgent, Roomba, ChargingStation
from mesa.visualization import CanvasGrid, BarChartModule
from mesa.visualization import ModularServer
from mesa.visualization import Slider

def agent_portrayal(agent):

    if agent is None: 
        return

    # Use a tuple of classes for the isinstance check
    if isinstance(agent, (ObstacleAgent, TrashAgent, Roomba, ChargingStation)):
        portrayal = {"Shape": "rect",
                    "Color": "black",
                    "Filled": "true",
                    "Layer": 1,
                    "w": 1,
                    "h": 1}

    if isinstance(agent, TrashAgent):
        portrayal = {"Shape": "circle",
                    "Color": "gray",
                    "Filled": "true",
                    "Layer": 2,
                    "r": 0.3}
    if isinstance(agent, Roomba):
        portrayal = {"Shape": "circle",
                    "Color": "#000000",
                    "Filled": "true",
                    "Layer": 3,
                    "r": 0.5}
    if isinstance(agent, ChargingStation):
        portrayal = {"Shape": "rect",
                    "Color": "red" if not agent.is_charging else "green",
                    "Filled": "true",
                    "Layer": 3,
                    "w": 1,
                    "h": 1}

    return portrayal

model_params = {"N":5, "width":10, "height":10, "amount_trash": Slider("Amount of trash", 5, 10, 15),} # N = número de agentes 

grid = CanvasGrid(agent_portrayal, 10, 10, 500, 500)


bar_chart = BarChartModule(
    [{"Label":"Steps", "Color":"#AA0000"}], 
    scope="agent", sorting="ascending", sort_by="Steps")

server = ModularServer(CleaningModel, [grid, bar_chart], "Cleaning Agents", model_params)        
server.port = 8222 # The default
server.launch()