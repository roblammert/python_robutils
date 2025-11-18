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

@staticmethod
def convert(value, from_unit, to_unit):
    if from_unit == to_unit:
        return value

    # Convert from the source unit to Celsius first
    if from_unit == UNITS.CELSIUS:
        celsius = value
    elif from_unit == UNITS.FAHRENHEIT:
        celsius = fahrenheit_to_celsius(value)
    elif from_unit == UNITS.KELVIN:
        celsius = kelvin_to_celsius(value)
    elif from_unit == UNITS.RANKINE:
        celsius = rankine_to_celsius(value)
    else:
        raise ValueError(f"Unsupported from_unit: {from_unit}")

    # Convert from Celsius to the target unit
    if to_unit == UNITS.CELSIUS:
        return celsius
    elif to_unit == UNITS.FAHRENHEIT:
        return celsius_to_fahrenheit(celsius)
    elif to_unit == UNITS.KELVIN:
        return celsius_to_kelvin(celsius)
    elif to_unit == UNITS.RANKINE:
        return celsius_to_rankine(celsius)
    else:
        raise ValueError(f"Unsupported to_unit: {to_unit}")

@staticmethod
def celsius_to_fahrenheit(celsius):
    return (celsius * 9/5) + 32

@staticmethod
def fahrenheit_to_celsius(fahrenheit):
    return (fahrenheit - 32) * 5/9

@staticmethod
def celsius_to_kelvin(celsius):
    return celsius + 273.15

@staticmethod
def kelvin_to_celsius(kelvin):
    return kelvin - 273.15

@staticmethod
def fahrenheit_to_kelvin(fahrenheit):
    return (fahrenheit + 459.67) * 5/9

@staticmethod
def kelvin_to_fahrenheit(kelvin):
    f = (kelvin * 9/5) - 459.67
    return (kelvin * 9/5) - 459.67

@staticmethod
def celsius_to_rankine(celsius):
    return (celsius + 273.15) * 9/5

@staticmethod
def rankine_to_celsius(rankine):
    return (rankine - 491.67) * 5/9

@staticmethod
def fahrenheit_to_rankine(fahrenheit):
    return fahrenheit + 459.67

@staticmethod
def rankine_to_fahrenheit(rankine):
    return rankine - 459.67