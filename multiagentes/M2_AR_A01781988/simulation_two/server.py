from model import CleaningModel, ObstacleAgent, TrashAgent, Roomba, ChargingStation
from mesa.visualization import CanvasGrid, BarChartModule, ChartModule
from mesa.visualization import ModularServer
from mesa.visualization import Slider

def agent_portrayal(agent):

    if agent is None: 
        return

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
                    "Color": "green",
                    "Filled": "true",
                    "Layer": 3,
                    "w": 1,
                    "h": 1}

    return portrayal

model_params = {"N": Slider("Number of Agents", 1, 2, 10), "width":10, "height":10, "amount_trash": Slider("Amount of trash", 5, 10, 15),"num_obstacles": Slider("Number of obstacles", 5,10,15)} # N = número de agentes 

grid = CanvasGrid(agent_portrayal, 10, 10, 500, 500)


bar_chart = BarChartModule(
    [{"Label": "Steps", "Color": "#AA0000"}], 
    scope="agent", sorting="ascending", sort_by="Steps")

bar_chart_clean = BarChartModule(
    [{"Label": "Cleaning percentage", "Color": "#0000FF"}], 
    scope="agent", sorting="ascending", sort_by="Cleaning percentage")

time_chart = ChartModule([{"Label": "Total Time", "Color": "#0000AA"}], data_collector_name="datacollector")

server = ModularServer(CleaningModel, [grid, bar_chart, bar_chart_clean, time_chart], "Cleaning Agents", model_params)        
server.port = 8222 # The default
server.launch()