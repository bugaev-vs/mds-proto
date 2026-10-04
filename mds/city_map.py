# city_map.py
from dataclasses import dataclass
from typing import List, Tuple, Optional
from shapely.geometry import LineString, Polygon, Point
from datetime import time

@dataclass
class Obstacle:
    obstacle_id: str
    transport_types: List[str]   # к каким средам относится
    geometry: object             # shapely Polygon или LineString
    active_from: time
    active_to: time
    severity: str = "full_block" # full_block / slowdown / restriction
    params: dict = None          # например {"max_height": 4.5}

class CityMap:
    def __init__(self):
        self.obstacles: List[Obstacle] = []
        # графы дорог для каждого типа транспорта
        self.graphs = {
            "sidewalk_rover": {},   # узел → список рёбер
            "autonomous_car": {},
            "water_vessel": {}
        }
    
    def add_obstacle(self, obs: Obstacle):
        self.obstacles.append(obs)
    
    def get_active_obstacles(self, transport_type: str, at_time: time) -> List[Obstacle]:
        result = []
        for obs in self.obstacles:
            if transport_type in obs.transport_types:
                if obs.active_from <= at_time <= obs.active_to:
                    result.append(obs)
        return result
