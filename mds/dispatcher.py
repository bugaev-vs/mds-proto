# dispatcher.py
from datetime import timedelta

from models import Decision, ApprovedRoute, RouteRequest
from occupancy import OccupancyMap
from checker import RouteChecker
from city_map import CityMap


class Dispatcher:
    """
    Главный диспетчер мультимодальной системы.

    Принимает заявки от клиентов, прогоняет их через RouteChecker
    для соответствующего типа транспорта, регистрирует согласованные
    маршруты в OccupancyMap и ведёт журнал всех заявок.
    """

    def __init__(self, city_map: CityMap):
        self.city_map = city_map
        self.occupancy = OccupancyMap()
        self.requests: dict = {}
        self.approved: list = []
        self.registered_clients: set = set()

    # ------------------------------------------------------------------
    # Регистрация клиентов
    # ------------------------------------------------------------------
    def register_client(self, client_id: str) -> None:
        """Добавляет клиента в список доверенных (магазин, аптека и т.п.)."""
        self.registered_clients.add(client_id)

    # ------------------------------------------------------------------
    # Обработка заявки
    # ------------------------------------------------------------------
    def submit_request(self, request: RouteRequest) -> dict:
        """
        Основной вход системы.

        1. Проверяет, что клиент зарегистрирован.
        2. Создаёт RouteChecker для нужной среды и запускает проверку.
        3. Если маршрут одобрен — регистрирует его в OccupancyMap.
        4. Возвращает словарь с результатом для API-ответа.
        """

        # --- 1. Регистрация клиента ---
        if request.client_id not in self.registered_clients:
            return {
                "request_id": request.request_id,
                "status": "rejected",
                "reason": "Клиент не зарегистрирован",
                "conflicts": [],
            }

        # Сохраняем заявку в журнал (даже если она будет отклонена)
        self.requests[request.request_id] = request

        # --- 2. Проверка маршрута ---
        checker = RouteChecker(
            self.city_map,
            self.occupancy,
            request.transport_type.value,
        )
        decision, reason, conflicts = checker.check(request)

        # Обновляем статус заявки (для аналитики)
        request.status = decision
        request.reason = reason

        # --- 3. Регистрация согласованного маршрута ---
        if decision in (Decision.APPROVED, Decision.APPROVED_WITH_CHANGES):
            route = ApprovedRoute(
                route_id=f"R-{len(self.approved) + 1:03d}",
                request_id=request.request_id,
                transport_type=request.transport_type,
                waypoints=request.waypoints,
                time_window=(
                    request.departure_time,
                    request.departure_time + timedelta(minutes=30),
                ),
            )
            self.occupancy.register(route)
            self.approved.append(route)

        # --- 4. Формируем ответ ---
        return {
            "request_id": request.request_id,
            "status": decision.value,
            "reason": reason,
            "conflicts": [
                c.obstacle_id if hasattr(c, "obstacle_id") else c
                for c in conflicts
            ],
        }

    # ------------------------------------------------------------------
    # Вспомогательные методы (пригодятся на защите / для аналитики)
    # ------------------------------------------------------------------
    def get_request(self, request_id: str) -> RouteRequest | None:
        """Вернуть заявку по её ID."""
        return self.requests.get(request_id)

    def get_approved_routes(self) -> list:
        """Список всех согласованных маршрутов."""
        return list(self.approved)

    def stats(self) -> dict:
        """Краткая сводка по журналу — удобно выводить в конце демо."""
        from collections import Counter

        statuses = Counter(r.status.value for r in self.requests.values())
        return {
            "total_requests": len(self.requests),
            "approved": len(self.approved),
            "by_status": dict(statuses),
            "clients": sorted(self.registered_clients),
        }
