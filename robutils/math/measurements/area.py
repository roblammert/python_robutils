# mypackage/math/measurements/area.py

"""Module for area measurement conversions and calculations."""

class UNITS:
    _SQUARE_INCH = "sq_in"
    _SQUARE_FOOT = "sq_ft"
    _SQUARE_YARD = "sq_yd"
    _ACRE = "acre"
    _SQUARE_MILE = "sq_mi"
    _SQUARE_MILLIMETER = "sq_mm"
    _SQUARE_CENTIMETER = "sq_cm"
    _SQUARE_METER = "sq_m"
    _SQUARE_HECTARE = "sq_ha"
    _SQUARE_KILOMETER = "sq_km"

def convert_area(value: float, from_unit: str, to_unit: str) -> float:
    """Convert area from one unit to another.

    Supported units:
    - Square Inch (sq_in)
    - Square Foot (sq_ft)
    - Square Yard (sq_yd)
    - Acre (acre)
    - Square Mile (sq_mi)
    - Square Millimeter (sq_mm)
    - Square Centimeter (sq_cm)
    - Square Meter (sq_m)
    - Square Hectare (sq_ha)
    - Square Kilometer (sq_km)

    Args:
        value (float): The area value to convert.
        from_unit (str): The unit of the input value.
        to_unit (str): The unit to convert the value to.

    Returns:
        float: The converted area value.
    """
    # Conversion factors to square meters
    conversion_to_sq_m = {
        UNITS._SQUARE_INCH: 0.00064516,
        UNITS._SQUARE_FOOT: 0.092903,
        UNITS._SQUARE_YARD: 0.836127,
        UNITS._ACRE: 4046.86,
        UNITS._SQUARE_MILE: 2589988.11,
        UNITS._SQUARE_MILLIMETER: 1e-6,
        UNITS._SQUARE_CENTIMETER: 1e-4,
        UNITS._SQUARE_METER: 1.0,
        UNITS._SQUARE_HECTARE: 10000.0,
        UNITS._SQUARE_KILOMETER: 1e6,
    }

    if from_unit not in conversion_to_sq_m or to_unit not in conversion_to_sq_m:
        raise ValueError("Unsupported unit for conversion.")

    # Convert from the original unit to square meters
    value_in_sq_m = value * conversion_to_sq_m[from_unit]
    # Convert from square meters to the target unit
    converted_value = value_in_sq_m / conversion_to_sq_m[to_unit]

    return converted_value

def calculate_triangle_area(base: float, height: float) -> float:
    """Calculate the area of a triangle.

    Args:
        base (float): The base length of the triangle.
        height (float): The height of the triangle.

    Returns:
        float: The area of the triangle.
    """
    return 0.5 * base * height

def calculate_circle_area(radius: float) -> float:
    """Calculate the area of a circle.

    Args:
        radius (float): The radius of the circle.

    Returns:
        float: The area of the circle.
    """
    import math
    return math.pi * radius ** 2