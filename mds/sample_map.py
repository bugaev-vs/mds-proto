from shapely.geometry import Polygon, LineString
from datetime import time

city = CityMap()

# --- Наземные препятствия (роверы) ---
city.add_obstacle(Obstacle(
    obstacle_id="stairs_1",
    transport_types=["sidewalk_rover"],
    geometry=Point(35, 42).buffer(0.5),
    active_from=time(0, 0), active_to=time(23, 59),
    severity="full_block",
    params={"reason": "Лестница на пути"}
))

city.add_obstacle(Obstacle(
    obstacle_id="narrow_1",
    transport_types=["sidewalk_rover"],
    geometry=LineString([(50,20), (60,20)]).buffer(0.2),
    active_from=time(0,0), active_to=time(23,59),
    severity="restriction",
    params={"min_width": 0.8}
))

city.add_obstacle(Obstacle(
    obstacle_id="crowd_lunch",
    transport_types=["sidewalk_rover"],
    geometry=Polygon([(70,30),(75,30),(75,35),(70,35)]),
    active_from=time(12,0), active_to=time(14,0),
    severity="slowdown",
    params={"density": "high", "delay_min": 10}
))

# --- Дорожные препятствия (автомобили) ---
city.add_obstacle(Obstacle(
    obstacle_id="excavation_1",
    transport_types=["autonomous_car"],
    geometry=LineString([(30,40),(30,60)]).buffer(2),
    active_from=time(8,0), active_to=time(20,0),
    severity="full_block",
    params={"reason": "Перекоп дороги"}
))

city.add_obstacle(Obstacle(
    obstacle_id="traffic_light_1",
    transport_types=["autonomous_car", "sidewalk_rover"],
    geometry=Point(50, 50).buffer(1),
    active_from=time(0,0), active_to=time(23,59),
    severity="slowdown",
    params={"cycle_green": 20, "cycle_red": 15, "avg_delay": 8}
))

# --- Воздушные препятствия ---
city.add_obstacle(Obstacle(
    obstacle_id="no_fly_hospital",
    transport_types=["aerial_drone"],
    geometry=Polygon([(40,40),(60,40),(60,60),(40,60)]),
    active_from=time(0,0), active_to=time(23,59),
    severity="full_block",
    params={"reason": "Больница — запретная зона"}
))

# --- Водные препятствия ---
city.add_obstacle(Obstacle(
    obstacle_id="drawbridge_1",
    transport_types=["water_vessel"],
    geometry=Point(60, 50).buffer(3),
    active_from=time(14,0), active_to=time(14,20),
    severity="restriction",
    params={"max_height": 3.0, "schedule": [("02:00","02:30"),("14:00","14:20")]}
))

city.add_obstacle(Obstacle(
    obstacle_id="shallow_1",
    transport_types=["water_vessel"],
    geometry=LineString([(20,60),(25,65)]).buffer(1),
    active_from=time(0,0), active_to=time(23,59),
    severity="restriction",
    params={"max_draft": 1.5}
))
