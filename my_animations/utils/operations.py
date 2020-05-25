import numpy as np
"""
This function will store any geometrical operations needed for animations
"""

def get_circle_intersection(origin_a, origin_b, r_1, r_2):
    """(numpy R^3 array, numpy R^3 array, float, float) -> numpy R^3 array

    Returns the intersection point(s) of two circles given the origin
    coordinates,origin_a and origin_b, of each circle and radii r_1, r_2

    pre-conditions:
        - The two given circles intersect at > 0 points
    """
    # For now we will be working in 2D space and will ignore the z
    # coordinate

    x_1, y_1, z_1 = origin_a
    x_2, y_2, z_2 = origin_b

    """
    Our algorithm,
    Strictly using algebraic equations of our circles,

        (1) (x-x_1)^2 + (y-y_1)^2 = r_1^2
        (2) (x-x_2)^2 + (y-y_2)^2 = r_2^2

    Subtracting (2) from (1) and magically rearranging we get,

        y = -[(x_1 - x_2)/(y_1 - y_2)]x +
            [(r_1^2-r_2^2)-(x_1^2-x_2^2)-(y_1^2-y_2^2)] / (y_1 - y_2)

            let v = [(r_1^2-r_2^2)-(x_1^2-x_2^2)-(y_1^2-y_2^2)] / -2 * (y_1 - y_2) so,

        (3) y =  -[(x_1 - x_2)/(y_1 - y_2)]x + v

    Substituting our y back into (1) and some more algebra we get the
    quadratic (if your thinking, that looks tedious, you are correct):

        (x-x_1)^2 + (-[(x_1 - x_2)/(y_1 - y_2)]x + v - y_1)^2 = r_1^2
        .
        .
        .
        Some quadratic formula

    Then use quadratic formula to solve for x, then use x in (3) to solve
    for y
    """

    # if origins of the two circles fall on the same axis
    if y_1 == y_2 and x_1 == x_2:
        raise ValueError("circles cannot be centred on the same origin")
    elif y_1 == y_2:
        # Denoting constant values in above formulas
        constant = (y_1-y_2)/(x_1-x_2)
        v = ((r_1**2-r_2**2)-(x_1**2-x_2**2)-(y_1**2-y_2**2)) / ((-2) * (x_1 - x_2))
        root = 'y'
    else:
        # Denoting constant values in above formulas
        constant = (x_1-x_2)/(y_1-y_2)
        v = ((r_1**2-r_2**2)-(x_1**2-x_2**2)-(y_1**2-y_2**2)) / ((-2) * (y_1 - y_2))
        root = 'x'

    if (root == 'x'):
         # quadratic formula to find roots along the x-axis
        a = (1.0 + constant**2)
        b = (-2) * (x_1 + (constant * (v - y_1)))
        c = x_1**2 + (v - y_1)**2  - r_1**2
        positive_x = ((-b) + np.sqrt(b**2 - 4*a*c)) / (2 * a)
        negative_x = ((-b) - np.sqrt(b**2 - 4*a*c)) / (2 * a)
        positive_y = (-constant) * positive_x + v
        negative_y = (-constant) * negative_x + v

    else:
        # quadratic formula to find the roots along the y-axis
        a = (1 + constant**2)
        b = -2 * (y_1 + (constant * (v - x_1)))
        c = y_1**2 + (v - x_1)**2  - r_1**2
        y = (-b + np.sqrt(b**2 - 4*a*c)) / 2 * a
        x = -(constant) * y + v
        positive_y = ((-b) + np.sqrt(b**2 - 4*a*c)) / (2 * a)
        negative_y = ((-b) - np.sqrt(b**2 - 4*a*c)) / (2 * a)
        positive_x = (-constant) * positive_y + v
        negative_x = (-constant) * negative_y + v

    return [np.array((positive_x, positive_y, 0)), np.array((negative_x, negative_y, 0))]
