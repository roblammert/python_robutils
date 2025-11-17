# mypackage/math/measurements/area.py

"""Module for area measurement conversions and calculations."""

def sq_meters_to_acres(sq_meters):
    """Converts area from square meters to acres."""
    return sq_meters * 0.000247105

def calculate_triangle_area(base, height):
    """Calculates the area of a triangle: A = 0.5 * base * height."""
    return 0.5 * base * height

def calculate_circle_area(radius):
    """Calculates the area of a circle: A = pi * r^2."""
    import math
    return math.pi * (radius**2)