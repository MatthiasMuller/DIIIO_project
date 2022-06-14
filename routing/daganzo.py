from math import sqrt

CONSTANT_PRODUCT_1 = 1.189
CONSTANT_PRODUCT_2 = 0.68


def daganzo_optimize(radius, number_of_points, capacity_vehicles, area_delivery):
    """
    This is the main function of the daganzo routing algorithm.
    """
    product_one = CONSTANT_PRODUCT_1 * (radius * (number_of_points / capacity_vehicles))
    product_two = CONSTANT_PRODUCT_2 * sqrt(area_delivery * number_of_points)
    return product_one + product_two
