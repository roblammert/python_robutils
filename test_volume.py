from robutils.math.measurements import volume as vol

def test_convert_volume():
    # Test conversion from cups to milliliters
    assert abs(vol.convert_volume(1, vol.UNITS._CUP, vol.UNITS._MILLILITER) - 236.588) < 0.001
    # Test conversion from liters to gallons
    assert abs(vol.convert_volume(1, vol.UNITS._LITER, vol.UNITS._GALLON) - 0.264172) < 0.0001
    # Test conversion from teaspoons to tablespoons
    assert abs(vol.convert_volume(3, vol.UNITS._TEASPOON, vol.UNITS._TABLESPOON) - 1) < 0.0001
    # Test conversion from pints to quarts
    assert abs(vol.convert_volume(2, vol.UNITS._PINT, vol.UNITS._QUART) - 1) < 0.0001
    # Test conversion from fluid ounces to cups
    assert abs(vol.convert_volume(8, vol.UNITS._FLUID_OUNCE, vol.UNITS._CUP) - 1) < 0.0001
    # Test conversion from milliliters to teaspoons
    assert abs(vol.convert_volume(4.92892, vol.UNITS._MILLILITER, vol.UNITS._TEASPOON) - 1) < 0.0001
    # Test conversion from gallons to liters
    assert abs(vol.convert_volume(1, vol.UNITS._GALLON, vol.UNITS._LITER) - 3.78541) < 0.0001
    # Test conversion from quarts to pints
    assert abs(vol.convert_volume(1, vol.UNITS._QUART, vol.UNITS._PINT) - 2) < 0.0001
    # Test conversion from tablespoons to fluid ounces
    assert abs(vol.convert_volume(2, vol.UNITS._TABLESPOON, vol.UNITS._FLUID_OUNCE) - 1) < 0.0001
    # Test conversion from cups to quarts
    assert abs(vol.convert_volume(4, vol.UNITS._CUP, vol.UNITS._QUART) - 1) < 0.0001
    print("All volume conversion tests passed.")

if __name__ == "__main__":
    test_convert_volume()