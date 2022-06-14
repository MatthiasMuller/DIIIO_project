import itertools
import math
import time
from random import randint

from constants import PRIMARY_DISPATCH_COST, SECONDARY_DISPATCH_COST, CONSTANT_ORDER_VOLUME, T
from dispatching.managers import VehicleManager, OrderManager, LocationManager
# VehicleManager
from dispatching.types import Order, Vehicle, State
# MAIN
from utils.plot import Plotter

veh_m = VehicleManager()
veh = veh_m.create_random()
print(f"Vehicle: {veh}")

# OrderManager
ord_m = OrderManager()
loc_m = LocationManager()

# plotter = Plotter()
# plotter.plot(orders=orders, center=CENTER)

initial_available_orders_amount = 3
available_vehicles: list[Vehicle] = [veh_m.create_random() for _ in range(5)]
plotter = Plotter()


def get_cost(s_t, order_combination):
    return 1


def create_random_new_orders(amount=None, t=None):
    if amount:
        return [ord_m.create_random(t=t) for _ in range(amount)]
    return [ord_m.create_random(t=t) for _ in range(randint(0, 2))]


def get_all_order_combinations(arr, t):
    shippable_orders = [order for order in arr if order["t_e"] <= t <= order["t_l"]]
    if CONSTANT_ORDER_VOLUME:
        return [shippable_orders[0:x] for x in range(0, len(shippable_orders) + 1)]
    res = []
    for l in range(0, len(shippable_orders)):
        for x in itertools.combinations(shippable_orders, l):
            res.append(list(x))
    return res


def get_used_vehicles(orders: [Order]) -> int:
    used_capacity = 0
    for order in orders:
        used_capacity += order["l"]
    used_vehicles_amount = math.ceil(used_capacity)
    return used_vehicles_amount


def get_available_vehicles(vehicles: [Vehicle]) -> [Vehicle]:
    return [vehicle for vehicle in vehicles if vehicle["remaining_periods"] == 0]


def get_decision_dispatch_cost(s_t: State, order_combination: [Order]) -> float:
    used_vehicles = get_used_vehicles(order_combination)
    routing_cost = loc_m.get_daganzo_cost(order_combination)
    available_primary_vehicles = get_available_vehicles(s_t["vehicles"])
    primary_available_vehicles_amount = len(available_primary_vehicles)
    decision_dispatch_cost = min(used_vehicles, primary_available_vehicles_amount) * PRIMARY_DISPATCH_COST + \
                             max(used_vehicles - primary_available_vehicles_amount, 0) * SECONDARY_DISPATCH_COST
    return decision_dispatch_cost + routing_cost


def get_not_dispatched_orders(s_t: State, order_combination: [Order]) -> [Order]:
    order_combination_ids = [order["id"] for order in order_combination]
    return [order for order in s_t["orders"] if order["id"] not in order_combination_ids]


def get_out_of_time_orders(s_t: State, t: int) -> bool:
    for order in s_t["orders"]:
        if order["t_l"] < t or t < order["t_e"]:
            return True
    return False


def get_final_cost(s_t: State) -> [float, [Order]]:
    if get_out_of_time_orders(s_t, t=T):
        return math.inf, []
    return [get_decision_dispatch_cost(s_t, s_t["orders"]), s_t["orders"]]


def c(s_t: State, t: int, new_orders_amount: int = None) -> [float, [Order]]:
    print(t)
    if t == T:
        return get_final_cost(s_t)
    if new_orders_amount:
        # Las ordenes que llegaron entre los dos periodos.
        s_t["orders"] += create_random_new_orders(new_orders_amount, t)

    order_combinations = get_all_order_combinations(s_t["orders"], t=t)

    min_cost_decision = math.inf
    min_cost_decision_order_combination = []

    for order_combination in order_combinations:
        decision_dispatch_cost = get_decision_dispatch_cost(s_t, order_combination)
        local_s_t = {
            "orders": get_not_dispatched_orders(s_t, order_combination),
            "vehicles": s_t["vehicles"]
        }
        # print(f"Dispatch cost: {decision_dispatch_cost}")
        dispatch_cost = decision_dispatch_cost + 1 / 3 * c(local_s_t, t + 1, new_orders_amount=1)[0] \
                        + 1 / 3 * c(local_s_t, t + 1, new_orders_amount=2)[0] \
                        + 1 / 3 * c(local_s_t, t + 1, new_orders_amount=3)[0]
        # print(f"Dispatch cost: {dispatch_cost}")
        if dispatch_cost < min_cost_decision:
            min_cost_decision = dispatch_cost
            min_cost_decision_order_combination = order_combination

    return min_cost_decision, min_cost_decision_order_combination


start_time = time.time()

decisions = []
state = {
    "orders": [ord_m.create_random(t=0) for _ in range(initial_available_orders_amount)],
    "vehicles": available_vehicles
}

min_cost, min_cost_combination = c(state, t=0)
print(min_cost, min_cost_combination)
decisions.append(min_cost_combination)
state["orders"] = get_not_dispatched_orders(state, min_cost_combination)

# plotter.plot(center=CENTER, orders=state["orders"])

end_time = time.time()

delivery_time = end_time - start_time

print(f"Execution time: {delivery_time}")
