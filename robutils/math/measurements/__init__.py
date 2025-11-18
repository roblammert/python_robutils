# mypackage/math/measurements/__init__.py

from .distance import convert_distance
from .volume import liters_to_gallons, calculate_sphere_volume
from .area import sq_meters_to_acres, calculate_triangle_area, calculate_circle_area
from .weight import kilograms_to_pounds, ounces_to_grams
from .temperature import celsius_to_fahrenheit, fahrenheit_to_celsius, celsius_to_kelvin, kelvin_to_celsius, convert_temperature, \
    fahrenheit_to_kelvin, kelvin_to_fahrenheit, celsius_to_rankine, rankine_to_celsius, fahrenheit_to_rankine, rankine_to_fahrenheit


# Define what happens during a 'from mypackage.math.measurements import *'
__all__ = [
    "meters_to_feet",
    "miles_to_kilometers",
    "calculate_euclidean_distance",
    "liters_to_gallons",
    "calculate_sphere_volume",
    "sq_meters_to_acres",
    "calculate_triangle_area",
    "calculate_circle_area",
    "kilograms_to_pounds",
    "ounces_to_grams",
    "celsius_to_fahrenheit",
    "fahrenheit_to_celsius",
    "celsius_to_kelvin",
    "kelvin_to_celsius",
    "convert",
    "fahrenheit_to_kelvin",
    "kelvin_to_fahrenheit",
    "celsius_to_rankine",
    "rankine_to_celsius",
    "fahrenheit_to_rankine",
    "rankine_to_fahrenheit",
]