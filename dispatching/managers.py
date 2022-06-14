import math
from random import randint, random

from constants import CENTER, VEHICLE_VOLUME, RADIUS, t_max, CONSTANT_ORDER_VOLUME, T
# Capacidad maxima del centro de consolidation
from dispatching.types import Vehicle, Order
from routing.daganzo import daganzo_optimize


class LocationManager:
    def get_radius_distance(self, v_x, v_y):
        return math.sqrt((v_x - CENTER[0]) ** 2 + (v_y - CENTER[1]) ** 2)

    def get_max_circular_radius_distance_in_list(self, orders: []) -> float:
        max_distance = 0
        for order in orders:
            distance = self.get_radius_distance(order["v_x"], order["v_y"])
            max_distance = max(max_distance, distance)
        return max_distance

    def get_area(self, radius: float) -> float:
        return math.pi * radius ** 2

    def get_daganzo_cost(self, orders: []):
        radius = self.get_max_circular_radius_distance_in_list(orders)
        area = self.get_area(radius)
        return daganzo_optimize(radius, len(orders), VEHICLE_VOLUME, area)


class OrderLocationManager:
    def create_random(self):
        alpha = 2 * math.pi * random()
        # random radius
        r = RADIUS * math.sqrt(random())
        # calculating coordinates
        x = r * math.cos(alpha) + CENTER[0]
        y = r * math.sin(alpha) + CENTER[1]
        return x, y


class VehicleManager:
    id = 0

    def create_random(self) -> Vehicle:
        _id = self.id
        self.id += 1
        return {
            "id": _id,
            "k": VEHICLE_VOLUME,
            "remaining_periods": 0,
        }


class OrderManager:
    id = 0
    location = OrderLocationManager()

    def create_random(self, t=0) -> Order:
        _id = self.id
        self.id += 1
        t_e = randint(t, t_max - 1)
        v = self.location.create_random()
        return {
            "id": _id,
            "t_e": t_e,
            # TODO: Check t_max
            "t_l": min(t_max, t_e + randint(0, T - t_e)),
            "l": CONSTANT_ORDER_VOLUME / VEHICLE_VOLUME,
            "v_x": v[0],
            "v_y": v[1],
        }
