# occupancy.py
from collections import defaultdict
from datetime import datetime, timedelta

from models import ApprovedRoute, TransportType


def _normalize(transport_type) -> str:
    """
    Приводит TransportType или строку к строковому ключу слоя.
    Защищает от KeyError, когда кто-то передаёт enum без .value.
    """
    if isinstance(transport_type, TransportType):
        return transport_type.value
    return str(transport_type)


class OccupancyMap:
    """
    Единая карта занятости коридоров.

    Хранит по слоям (среда) список занятий сегментов маршрутов.
    Ключ сегмента — нормализованная пара точек, порядок не важен.
    """

    def __init__(self):
        self.layers = {
            "sidewalk_rover": defaultdict(list),
            "autonomous_car": defaultdict(list),
            "aerial_drone": defaultdict(list),
            "water_vessel": defaultdict(list),
        }

    # ------------------------------------------------------------------
    # Ключ сегмента
    # ------------------------------------------------------------------
    def _segment_key(self, p1, p2) -> str:
        a = (round(p1.x, 1), round(p1.y, 1))
        b = (round(p2.x, 1), round(p2.y, 1))
        return f"{min(a, b)}__{max(a, b)}"

    # ------------------------------------------------------------------
    # Регистрация согласованного маршрута
    # ------------------------------------------------------------------
    def register(self, route: ApprovedRoute) -> None:
        layer = self.layers[_normalize(route.transport_type)]
        for i in range(len(route.waypoints) - 1):
            key = self._segment_key(
                route.waypoints[i], route.waypoints[i + 1]
            )
            layer[key].append({
                "route_id": route.route_id,
                "time": route.time_window,
                "width": route.corridor_width,
            })

    # ------------------------------------------------------------------
    # Загрузка коридора на момент времени
    # ------------------------------------------------------------------
    def get_load(self, transport_type, waypoints, at_time: datetime) -> int:
        layer = self.layers[_normalize(transport_type)]
        max_load = 0
        window = (at_time, at_time + timedelta(minutes=20))

        for i in range(len(waypoints) - 1):
            key = self._segment_key(waypoints[i], waypoints[i + 1])
            count = sum(
                1 for entry in layer.get(key, [])
                if self._overlap(entry["time"], window)
            )
            max_load = max(max_load, count)

        return max_load

    # ------------------------------------------------------------------
    # Пересечение временных окон
    # ------------------------------------------------------------------
    def _overlap(self, t1, t2) -> bool:
        return not (t1[1] < t2[0] or t2[1] < t1[0])
