import matplotlib.pyplot as plt
import numpy as np
from gurobipy import Model, GRB, quicksum


# Optimiza la ruta según el algoritmo de vrp mas comun.
def vrp_optimize():
    rnd = np.random
    rnd.seed(0)

    n = 8  # number of clients
    # clients_location = {
    #     "A": [-33.34153820682023, -70.52148385460123],
    #     "B": [-33.366845947734674, -70.5446581393933],
    #     "C": [-33.38755983760026, -70.55298371608706],
    # }
    xc = rnd.rand(n + 1) * 1500  # x-coordinate of clients and the depot
    yc = rnd.rand(n + 1) * 2500  # y-coordinate of clients and the depot
    # print(xc, yc)

    # xc = [0, ]  # x-coordinate of clients and the depot
    # yc = [0, ]  # y-coordinate of clients and the depot
    #
    # for key, value in clients_location.items():
    #     xc.append(value[0])
    #     yc.append(value[1])

    xc[0] = -33.36820791234188  # Set the depot to a very far location
    yc[0] = -70.50191445936937  # Set the depot to a very far location

    N = [i for i in range(1, n + 1)]  # Customers
    V = [0] + N
    A = [(i, j) for i in V for j in V if i != j]  # Edges between each pair of dots
    c = {(i, j): np.hypot(xc[i] - xc[j], yc[i] - yc[j]) for i, j in A}  # Distance
    Q = 20  # vehicle capacity
    q = {i: rnd.randint(1, 10) for i in N}  # Demand from each customer

    mdl = Model('CVRP')
    x = mdl.addVars(A, vtype=GRB.BINARY)  # Decision variable for whether an edge should be chosen.
    u = mdl.addVars(N, vtype=GRB.CONTINUOUS)  # load of vehicle before it leaves the node

    mdl.modelSense = GRB.MINIMIZE
    mdl.setObjective(quicksum(x[i, j] * c[i, j] for (i, j) in A))

    mdl.addConstrs(
        quicksum(x[i, j] for j in V if j != i) == 1 for i in N)  # only one edge into customer node i
    mdl.addConstrs(
        quicksum(x[i, j] for i in V if i != j) == 1 for j in N)  # only one edge out of customer node i
    mdl.addConstrs((x[i, j] == 1) >> (u[i] + q[i] == u[j]) for i, j in A if i != 0 and j != 0)
    mdl.addConstrs(u[i] >= q[i] for i in N)
    mdl.addConstrs(u[i] <= Q for i in N)

    mdl.optimize()

    return mdl, x, u, xc, yc, A, c, q


def plot(xc, yc, A, x):
    active_arcs = [a for a in A if x[a].X > 0.9]

    for i, j in active_arcs:
        # Lines
        plt.plot([xc[i], xc[j]], [yc[i], yc[j]], c='g', zorder=0)
    # Depot
    plt.plot(xc[0], yc[0], c='r', marker='s')  # Location of the depot
    # Clients
    plt.scatter(xc[1:], yc[1:], c='b')  # Location of clients

    plt.show()
