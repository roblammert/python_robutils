# mypackage/math/measurements/weight.py

"""Module for mass and weight measurement conversions."""

class UNIT:
    _OUNCE = 'ounce' #avoirdupois ounce
    _SLUG = 'slug'
    _POUND = 'pound'
    _TON_US = 'ton_us'  # US ton
    _TON_UK = 'ton_uk'    # UK ton
    _GRAM = 'gram'
    _KILOGRAM = 'kilogram'
    _TONNE = 'tonne'  # metric ton
    
    @property
    def OUNCE(self):
        return self._OUNCE
    @property
    def SLUG(self):
        return self._SLUG
    @property
    def POUND(self):
        return self._POUND
    @property
    def TON_US(self):
        return self._TON_US
    @property
    def TON_UK(self):
        return self._TON_UK
    @property
    def GRAM(self):
        return self._GRAM
    @property
    def KILOGRAM(self):
        return self._KILOGRAM
    @property
    def TONNE(self):
        return self._TONNE

def convert_weight(value, from_unit, to_unit):
    """Converts a mass from one unit to another."""
    # Conversion factors to kilograms
    to_kilograms = {
        UNIT.OUNCE: 0.0283495,
        UNIT.SLUG: 14.5939,
        UNIT.POUND: 0.453592,
        UNIT.TON_US: 907.185,
        UNIT.TON_UK: 1016.05,
        UNIT.GRAM: 0.001,
        UNIT.KILOGRAM: 1.0,
        UNIT.TONNE: 1000.0,
    }

    # Convert from the source unit to kilograms
    value_in_kilograms = value * to_kilograms[from_unit]
    # Convert from kilograms to the target unit
    converted_value = value_in_kilograms / to_kilograms[to_unit]
    return converted_value