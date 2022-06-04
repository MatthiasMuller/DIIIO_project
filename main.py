import itertools
import math
import time
from random import randint

from constants import PRIMARY_DISPATCH_COST, SECONDARY_DISPATCH_COST
from dispatching.managers import VehicleManager, OrderManager
# VehicleManager
from dispatching.types import Order, Vehicle, State

# MAIN

veh_m = VehicleManager()
veh = veh_m.create_random()
print(f"Vehicle: {veh}")

# OrderManager
ord_m = OrderManager()

# plotter = Plotter()
# plotter.plot(orders=orders, center=CENTER)
T: int = 7

available_orders: list[Order] = []
available_vehicles: list[Vehicle] = [veh_m.create_random() for _ in range(2)]


def get_cost(s_t, order_combination):
    return 1


def create_random_new_orders(amount=None, t=None):
    if amount:
        return [ord_m.create_random(t=t) for _ in range(amount)]
    return [ord_m.create_random(t=t) for _ in range(randint(0, 2))]


def get_all_order_combinations(arr):
    res = []
    for l in range(2, len(arr)):
        for x in itertools.combinations(arr, l):
            res.append(list(x))
    return res


def get_used_vehicles(orders: [Order]) -> int:
    used_capacity = 0
    for order in orders:
        used_capacity += order["l"]
    used_vehicles_amount = math.ceil(used_capacity)
    return used_vehicles_amount


def get_decision_dispatch_cost(s_t: State, order_combination: [Order]) -> int:
    used_vehicles = get_used_vehicles(order_combination)
    decision_dispatch_cost = min(used_vehicles, len(s_t["vehicles"])) * PRIMARY_DISPATCH_COST + \
                             max(used_vehicles - len(s_t["vehicles"]), 0) * SECONDARY_DISPATCH_COST
    return decision_dispatch_cost


def get_not_dispatched_orders(s_t: State, order_combination: [Order]) -> [Order]:
    order_combination_ids = [order["id"] for order in order_combination]
    if len(order_combination) != len([order for order in s_t["orders"] if order["id"] in order_combination_ids]):
        print(order_combination, [order for order in s_t["orders"] if order["id"] in order_combination_ids])
    return [order for order in s_t["orders"] if order["id"] in order_combination_ids]


def c(s_t: State, t: int, new_orders_amount: int = None) -> float:
    if t == T:
        return get_decision_dispatch_cost(s_t, s_t["orders"])
    print(t)

    # Las ordenes que llegaron entre los dos periodos.
    s_t["orders"] += create_random_new_orders(new_orders_amount, t)

    order_combinations = get_all_order_combinations(s_t["orders"])
    order_combinations.append([])

    min_cost_decision = math.inf

    for order_combination in order_combinations:
        decision_dispatch_cost = get_decision_dispatch_cost(s_t, order_combination)
        local_s_t = {
            "orders": get_not_dispatched_orders(s_t, order_combination),
            "vehicles": s_t["vehicles"]
        }
        # print(f"Dispatch cost: {decision_dispatch_cost}")
        dispatch_cost = decision_dispatch_cost + 1 / 3 * c(local_s_t, t + 1, new_orders_amount=1) \
                        + 1 / 3 * c(local_s_t, t + 1, new_orders_amount=2) \
                        + 1 / 3 * c(local_s_t, t + 1, new_orders_amount=3)
        # print(f"Dispatch cost: {dispatch_cost}")
        min_cost_decision = min(min_cost_decision, dispatch_cost)

    return min_cost_decision


start_time = time.time()

min_cost = c({"orders": [], "vehicles": [veh_m.create_random() for i in range(2)]}, 0)

end_time = time.time()

delivery_time = end_time - start_time

print(f"Min cost: {min_cost}")
print(f"Delivery time: {delivery_time}")
