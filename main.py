# #############################################################################

# CONSTANTS
l_max: int = 10
# Max window
t_max: int = 10
# Cap_vehiculo
VEHICLE_VOLUME: int = 10
# Center of the map
CENTER = [-33.346815030265034, -70.52199644371268]
# Radius of the map
RADIUS = 0.0005

# #############################################################################
# MAIN

if __name__ == '__main__':
    from dispatching.managers import VehicleManager, OrderManager

    # VehicleManager
    veh_m = VehicleManager()
    veh = veh_m.create_random()
    print(f"Vehicle: {veh}")

    # OrderManager
    ord_m = OrderManager()
    for i in range(10):
        ord = ord_m.create_random()
        print(f"Order: {ord}")
