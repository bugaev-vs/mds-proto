import sys
print(">>> Python:", sys.executable)

from datetime import datetime, timedelta
from models import RouteRequest, Waypoint, TransportType
from city_map import CityMap, Obstacle
from dispatcher import Dispatcher
from shapely.geometry import Polygon, LineString, Point
from datetime import time


def run_demo():
    # --- 1. Создание карты ---
    city = CityMap()

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
        geometry=LineString([(50, 20), (60, 20)]).buffer(0.2),
        active_from=time(0, 0), active_to=time(23, 59),
        severity="restriction",
        params={"min_width": 0.8}
    ))

    city.add_obstacle(Obstacle(
        obstacle_id="crowd_lunch",
        transport_types=["sidewalk_rover"],
        geometry=Polygon([(70, 30), (75, 30), (75, 35), (70, 35)]),
        active_from=time(12, 0), active_to=time(14, 0),
        severity="slowdown",
        params={"density": "high", "delay_min": 10}
    ))

    city.add_obstacle(Obstacle(
        obstacle_id="excavation_1",
        transport_types=["autonomous_car"],
        geometry=LineString([(30, 40), (30, 60)]).buffer(2),
        active_from=time(8, 0), active_to=time(20, 0),
        severity="full_block",
        params={"reason": "Перекоп дороги"}
    ))

    city.add_obstacle(Obstacle(
        obstacle_id="traffic_light_1",
        transport_types=["autonomous_car", "sidewalk_rover"],
        geometry=Point(50, 50).buffer(1),
        active_from=time(0, 0), active_to=time(23, 59),
        severity="slowdown",
        params={"cycle_green": 20, "cycle_red": 15, "avg_delay": 8}
    ))

    city.add_obstacle(Obstacle(
        obstacle_id="no_fly_hospital",
        transport_types=["aerial_drone"],
        geometry=Polygon([(40, 40), (60, 40), (60, 60), (40, 60)]),
        active_from=time(0, 0), active_to=time(23, 59),
        severity="full_block",
        params={"reason": "Больница — запретная зона"}
    ))

    city.add_obstacle(Obstacle(
        obstacle_id="drawbridge_1",
        transport_types=["water_vessel"],
        geometry=Point(60, 50).buffer(3),
        active_from=time(14, 0), active_to=time(14, 20),
        severity="restriction",
        params={"max_height": 3.0,
                "schedule": [("02:00", "02:30"), ("14:00", "14:20")]}
    ))

    city.add_obstacle(Obstacle(
        obstacle_id="shallow_1",
        transport_types=["water_vessel"],
        geometry=LineString([(20, 60), (25, 65)]).buffer(1),
        active_from=time(0, 0), active_to=time(23, 59),
        severity="restriction",
        params={"max_draft": 1.5}
    ))

    # --- 2. Диспетчер ---
    dispatcher = Dispatcher(city)                    # ← вот эта строка
    dispatcher.register_client("pizza_shop")
    dispatcher.register_client("pharmacy")

    t0 = datetime(2025, 6, 1, 14, 0)

    # --- 3. Сценарии ---
    scenarios = [
        RouteRequest(
            request_id="REQ-001", client_id="pizza_shop",
            transport_type=TransportType.SIDEWALK_ROVER,
            waypoints=[Waypoint(10, 10), Waypoint(20, 15), Waypoint(30, 25)],
            departure_time=t0,
            vehicle_params={"width": 0.9}
        ),
        RouteRequest(
            request_id="REQ-002", client_id="pharmacy",
            transport_type=TransportType.SIDEWALK_ROVER,
            waypoints=[Waypoint(30, 40), Waypoint(35, 42), Waypoint(40, 45)],
            departure_time=t0,
            vehicle_params={"width": 0.9}
        ),
        RouteRequest(
            request_id="REQ-003", client_id="pizza_shop",
            transport_type=TransportType.AUTONOMOUS_CAR,
            waypoints=[Waypoint(25, 35), Waypoint(30, 50), Waypoint(35, 65)],
            departure_time=t0,
            vehicle_params={"height": 1.8, "mass": 1500}
        ),
        RouteRequest(
            request_id="REQ-004", client_id="pharmacy",
            transport_type=TransportType.AERIAL_DRONE,
            waypoints=[Waypoint(35, 45), Waypoint(50, 50), Waypoint(65, 55)],
            departure_time=t0,
            vehicle_params={"max_alt": 120, "payload": 2}
        ),
        RouteRequest(
            request_id="REQ-005", client_id="pizza_shop",
            transport_type=TransportType.WATER_VESSEL,
            waypoints=[Waypoint(15, 55), Waypoint(22, 62), Waypoint(30, 70)],
            departure_time=t0,
            vehicle_params={"draft": 2.0, "height": 4.0}
        ),
    ]

    # --- 4. Обработка ---
    for req in scenarios:
        result = dispatcher.submit_request(req)
        print(f"\n[{result['request_id']}] {result['status']}")
        print(f"   Причина: {result['reason']}")
        if result['conflicts']:
            print(f"   Конфликты: {result['conflicts']}")

    # --- 5. Визуализация ---
    from visualize import draw_city
    from gantt import draw_gantt
    from analytics import draw_load_analytics

    draw_city(city, dispatcher)
    draw_gantt(dispatcher)
    draw_load_analytics(dispatcher)

if __name__ == "__main__":
    run_demo()
