# mypackage/math/measurements/volume.py

"""Module for volume measurement conversions and calculations."""

import math

def liters_to_gallons(liters):
    """Converts a volume from liters to US liquid gallons."""
    return liters * 0.264172

def calculate_sphere_volume(radius):
    """
    Calculates the volume of a sphere. Formula: V = (4/3) * pi * r^3
    """
    return (4/3) * math.pi * (radius**3)