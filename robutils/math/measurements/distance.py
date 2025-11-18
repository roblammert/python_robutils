# mypackage/math/measurements/distance.py

"""Module for distance and length measurement conversions."""

class UNIT:
    _MILE = 'mile'
    _YARD = 'yard'
    _FOOT = 'foot'
    _INCH = 'inch'
    _KILOMETER = 'kilometer'
    _METER = 'meter'
    _CENTIMETER = 'centimeter'
    _MILLIMETER = 'millimeter'

    @property
    def MILE(self):
        return self._MILE
    @property
    def YARD(self):
        return self._YARD
    @property
    def FOOT(self):
        return self._FOOT
    @property
    def INCH(self):
        return self._INCH
    @property
    def KILOMETER(self):
        return self._KILOMETER
    @property
    def METER(self):
        return self._METER
    @property
    def CENTIMETER(self):
        return self._CENTIMETER
    @property
    def MILLIMETER(self):
        return self._MILLIMETER



def convert_distance(value, from_unit, to_unit):
    """Converts a length from one unit to another."""
    # Conversion factors to meters
    to_meters = {
        UNIT.MILE: 1609.34,
        UNIT.YARD: 0.9144,
        UNIT.FOOT: 0.3048,
        UNIT.INCH: 0.0254,
        UNIT.KILOMETER: 1000.0,
        UNIT.METER: 1.0,
        UNIT.CENTIMETER: 0.01,
        UNIT.MILLIMETER: 0.001,
    }

    # Convert from the source unit to meters
    value_in_meters = value * to_meters[from_unit]
    # Convert from meters to the target unit
    converted_value = value_in_meters / to_meters[to_unit]
    return converted_value

