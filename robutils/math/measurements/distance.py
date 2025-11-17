# mypackage/math/measurements/distance.py

"""Module for distance and length measurement conversions."""

def meters_to_feet(meters):
    """Converts a length from meters to feet."""
    return meters * 3.28084

def miles_to_kilometers(miles):
    """Converts a distance from miles to kilometers."""
    return miles * 1.60934

def calculate_euclidean_distance(p1, p2):
    """
    Calculates the Euclidean distance between two 2D points.

    Args:
        p1 (tuple): (x1, y1)
        p2 (tuple): (x2, y2)
    """
    x1, y1 = p1
    x2, y2 = p2
    return ((x2 - x1)**2 + (y2 - y1)**2)**0.5