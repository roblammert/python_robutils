# mypackage/math/measurements/temperature.py
"""Module for temperature measurement conversions."""



class UNITS:
    _CELSIUS = 'Celsius'
    _FAHRENHEIT = 'Fahrenheit'
    _KELVIN = 'Kelvin'
    _RANKINE = 'Rankine'

    @property
    def CELSIUS():
        global _CELSIUS
        return _CELSIUS
    @property
    def FAHRENHEIT():
        global _FAHRENHEIT
        return _FAHRENHEIT
    @property
    def KELVIN():
        global _KELVIN
        return _KELVIN
    @property
    def RANKINE():
        global _RANKINE
        return _RANKINE

def convert_temperature(value: float, from_unit: str, to_unit: str) -> float:
    """Convert temperature between different units.

    Args:
        value (float): The temperature value to convert.
        from_unit (str): The unit of the input temperature.
        to_unit (str): The unit to convert the temperature to.

    Returns:
        float: The converted temperature value.
    """
    to_celsius = {
        UNITS.CELSIUS: lambda x: x,
        UNITS.FAHRENHEIT: lambda x: (x - 32) * 5.0 / 9.0,
        UNITS.KELVIN: lambda x: x - 273.15,
        UNITS.RANKINE: lambda x: (x - 491.67) * 5.0 / 9.0,
    }
    from_celsius = {
        UNITS.CELSIUS: lambda x: x,
        UNITS.FAHRENHEIT: lambda x: (x * 9.0 / 5.0) + 32,
        UNITS.KELVIN: lambda x: x + 273.15,
        UNITS.RANKINE: lambda x: (x * 9.0 / 5.0) + 491.67,
    }
    celsius_value = to_celsius[from_unit](value)
    return from_celsius[to_unit](celsius_value)