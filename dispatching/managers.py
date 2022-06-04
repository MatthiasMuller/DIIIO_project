from random import randint

from constants import CENTER, VEHICLE_VOLUME, RADIUS, t_max
# Capacidad maxima del centro de consolidation
from dispatching.types import Vehicle, Order


class LocationManager:
    def create_random(self):
        x = CENTER[0] + (randint(-1000, 1000) * RADIUS / 1000)
        y = CENTER[1] + (randint(-1000, 1000) * RADIUS / 1000)
        return x, y


class VehicleManager:
    id = 0

    def create_random(self) -> Vehicle:
        _id = self.id
        self.id += 1
        return {
            "id": _id,
            "k": VEHICLE_VOLUME,
            "available": True,
        }


class OrderManager:
    id = 0
    location = LocationManager()

    def create_random(self, t=0) -> Order:
        _id = self.id
        self.id += 1
        t_e = randint(t, t_max - 1)
        _vol = randint(1, VEHICLE_VOLUME)
        v = self.location.create_random()
        return {
            "id": _id,
            "t_e": t_e,
            "t_l": t_e + randint(0, t_max - t_e),
            "l": _vol / VEHICLE_VOLUME,
            "v_x": v[0],
            "v_y": v[1],
        }
