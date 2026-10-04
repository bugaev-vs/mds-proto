# checker.py
from datetime import datetime, timedelta
from typing import List, Tuple

from shapely.geometry import LineString, Point

from models import RouteRequest, Decision


class RouteChecker:
    """
    Проверяет заявку для конкретной среды (тротуар / дорога / воздух / вода).

    Различия сред — только в наборе препятствий из CityMap и в лимите
    пропускной способности (_max_capacity). Логика одна и та же.
    """

    def __init__(self, city_map, occupancy, transport_type: str):
        # transport_type здесь — строка, например "sidewalk_rover"
        self.city_map = city_map
        self.occupancy = occupancy
        self.transport_type = transport_type

    # ------------------------------------------------------------------
    # Основная проверка
    # ------------------------------------------------------------------
    def check(self, request: RouteRequest) -> Tuple[Decision, str, List]:
        conflicts = []
        recommendations = []

        route_line = LineString([(wp.x, wp.y) for wp in request.waypoints])
        t = request.departure_time.time()

        # 1. Геометрические пересечения с активными препятствиями
        for obs in self.city_map.get_active_obstacles(self.transport_type, t):
            if self._intersects(route_line, obs, request):
                conflicts.append(obs)
                recommendations.append(self._make_recommendation(obs, request))

        # 2. Проверка занятости коридора
        load = self.occupancy.get_load(
            self.transport_type,          # строка, а не enum
            request.waypoints,
            request.departure_time,
        )
        if load >= self._max_capacity():
            conflicts.append("OVERLOAD")
            recommendations.append("Сдвинуть вылет на 15 минут")

        # 3. Решение
        if not conflicts:
            return Decision.APPROVED, "Маршрут свободен", []
        elif all(recommendations):
            return (
                Decision.APPROVED_WITH_CHANGES,
                "; ".join(recommendations),
                conflicts,
            )
        else:
            return (
                Decision.REJECTED,
                "Маршрут невозможен: " + "; ".join(recommendations),
                conflicts,
            )

    # ------------------------------------------------------------------
    # Проверка пересечения с учётом параметров транспорта
    # ------------------------------------------------------------------
    def _intersects(self, route_line, obstacle, request) -> bool:
        if not route_line.intersects(obstacle.geometry):
            return False

        params = obstacle.params or {}
        vp = request.vehicle_params or {}

        if "max_height" in params and vp.get("height", 0) > params["max_height"]:
            return True
        if "max_draft" in params and vp.get("draft", 0) > params["max_draft"]:
            return True
        if "min_width" in params and vp.get("width", 0) > params["min_width"]:
            return True

        return True

    # ------------------------------------------------------------------
    # Рекомендация по конкретному препятствию
    # ------------------------------------------------------------------
    def _make_recommendation(self, obs, request) -> str:
        if obs.severity == "full_block":
            return f"Объезд препятствия {obs.obstacle_id}"
        if obs.severity == "slowdown":
            return f"Замедление из-за {obs.obstacle_id}"
        if obs.severity == "restriction":
            return (
                f"Ограничение: {obs.obstacle_id} "
                f"(нужно изменить маршрут или время)"
            )
        return "Проверить маршрут"

    # ------------------------------------------------------------------
    # Пропускная способность по средам
    # ------------------------------------------------------------------
    def _max_capacity(self) -> int:
        return {
            "sidewalk_rover": 2,
            "autonomous_car": 3,
            "aerial_drone": 4,
            "water_vessel": 1,
        }[self.transport_type]
