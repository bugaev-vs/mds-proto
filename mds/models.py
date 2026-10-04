# models.py
from dataclasses import dataclass, field
from enum import Enum
from typing import List, Tuple, Optional
from datetime import datetime, timedelta

class TransportType(Enum):
    SIDEWALK_ROVER = "sidewalk_rover"   # тротуарный ровер
    AUTONOMOUS_CAR = "autonomous_car"   # беспилотный автомобиль
    AERIAL_DRONE   = "aerial_drone"     # воздушный дрон
    WATER_VESSEL   = "water_vessel"     # водный катер

class Decision(Enum):
    APPROVED = "approved"
    APPROVED_WITH_CHANGES = "approved_with_changes"
    REJECTED = "rejected"
    PENDING = "pending"

@dataclass
class Waypoint:
    x: float
    y: float
    z: float = 0.0          # высота (для дронов) или глубина (для катеров)
    tag: Optional[str] = None   # "stairs", "bridge", "lock", "traffic_light"

@dataclass
class RouteRequest:
    request_id: str
    client_id: str
    transport_type: TransportType
    waypoints: List[Waypoint]
    departure_time: datetime
    cargo_weight: float = 1.0
    vehicle_params: dict = field(default_factory=dict)
    # для ровера: {"width": 0.9, "max_slope": 15}
    # для авто:  {"height": 1.8, "mass": 1500}
    # для дрона: {"max_alt": 120, "payload": 5}
    # для катера: {"draft": 1.5, "height": 4.0}
    status: Decision = Decision.PENDING
    reason: str = ""

@dataclass
class ApprovedRoute:
    route_id: str
    request_id: str
    transport_type: TransportType
    waypoints: List[Waypoint]
    time_window: Tuple[datetime, datetime]
    corridor_width: float = 3.0
    segments: List[str] = field(default_factory=list)  # ID сегментов
