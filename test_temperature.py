from robutils.math.measurements import temperature as temp

def test_temperature_conversions():
    
    # Test general conversion function
    assert abs(temp.convert_temperature(0, temp.UNITS.CELSIUS, temp.UNITS.FAHRENHEIT) - 32) < 1e-6
    assert abs(temp.convert_temperature(32, temp.UNITS.FAHRENHEIT, temp.UNITS.CELSIUS) - 0) < 1e-6
    assert abs(temp.convert_temperature(0, temp.UNITS.CELSIUS, temp.UNITS.KELVIN) - 273.15) < 1e-6
    assert abs(temp.convert_temperature(273.15, temp.UNITS.KELVIN, temp.UNITS.CELSIUS) - 0) < 1e-6
    assert abs(temp.convert_temperature(32, temp.UNITS.FAHRENHEIT, temp.UNITS.KELVIN) - 273.15) < 1e-6
    assert abs(temp.convert_temperature(273.15, temp.UNITS.KELVIN, temp.UNITS.FAHRENHEIT) - 32) < 1e-6
    assert abs(temp.convert_temperature(0, temp.UNITS.CELSIUS, temp.UNITS.RANKINE) - 491.67) < 1e-6
    assert abs(temp.convert_temperature(491.67, temp.UNITS.RANKINE, temp.UNITS.CELSIUS) - 0) < 1e-6
    assert abs(temp.convert_temperature(32, temp.UNITS.FAHRENHEIT, temp.UNITS.RANKINE) - 491.67) < 1e-6
    assert abs(temp.convert_temperature(491.67, temp.UNITS.RANKINE, temp.UNITS.FAHRENHEIT) - 32) < 1e-6

    print("All temperature conversion tests passed!")

if __name__ == "__main__":
    test_temperature_conversions()