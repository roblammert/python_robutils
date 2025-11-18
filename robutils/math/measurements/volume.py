# mypackage/math/measurements/volume.py

"""Module for volume measurement conversions and calculations."""

class UNITS:
    _TEASPOON = "tsp"
    _TABLESPOON = "tbsp"
    _CUP = "cup"
    _FLUID_OUNCE = "fl_oz"
    _PINT = "pt"
    _QUART = "qt"
    _GALLON = "gal"
    _LITER = "l"
    _MILLILITER = "ml"

def convert_volume(value: float, from_unit: str, to_unit: str) -> float:
    """Convert volume from one unit to another.

    Supported units:
    - Teaspoon (tsp)
    - Tablespoon (tbsp)
    - Cup (cup)
    - Fluid Ounce (fl_oz)
    - Pint (pt)
    - Quart (qt)
    - Gallon (gal)
    - Liter (l)
    - Milliliter (ml)

    Args:
        value (float): The volume value to convert.
        from_unit (str): The unit of the input value.
        to_unit (str): The unit to convert the value to.

    Returns:
        float: The converted volume value.
    """
    # Conversion factors to milliliters
    conversion_to_ml = {
        UNITS._TEASPOON: 4.92892,
        UNITS._TABLESPOON: 14.7868,
        UNITS._CUP: 236.588,
        UNITS._FLUID_OUNCE: 29.5735,
        UNITS._PINT: 473.176,
        UNITS._QUART: 946.353,
        UNITS._GALLON: 3785.41,
        UNITS._LITER: 1000.0,
        UNITS._MILLILITER: 1.0,
    }

    if from_unit not in conversion_to_ml or to_unit not in conversion_to_ml:
        raise ValueError("Unsupported unit for conversion.")

    # Convert from the original unit to milliliters
    value_in_ml = value * conversion_to_ml[from_unit]
    # Convert from milliliters to the target unit
    converted_value = value_in_ml / conversion_to_ml[to_unit]

    return converted_value