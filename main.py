from dispatching.managers import VehicleManager, OrderManager

# MAIN

if __name__ == '__main__':
    # VehicleManager
    veh_m = VehicleManager()
    veh = veh_m.create_random()
    print(f"Vehicle: {veh}")

    # OrderManager
    ord_m = OrderManager()
    orders = [ord_m.create_random() for _ in range(10)]
    for i in orders:
        print(f"Order: {i}")





    # plotter = Plotter()
    # plotter.plot(orders=orders, center=CENTER)
