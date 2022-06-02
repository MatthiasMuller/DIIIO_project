from typing import TypedDict


class Order(TypedDict):
    id: int
    t_e: int
    t_l: int
    l: float
    v_x: float
    v_y: float


class Vehicle(TypedDict):
    id: int
    k: int
