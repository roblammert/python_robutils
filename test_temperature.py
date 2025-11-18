from robutils.math.measurements import temperature as temp

def test_temperature_conversions():
    # Celsius to Fahrenheit
    assert temp.celsius_to_fahrenheit(0) == 32
    assert temp.celsius_to_fahrenheit(100) == 212

    # Fahrenheit to Celsius
    assert temp.fahrenheit_to_celsius(32) == 0
    assert temp.fahrenheit_to_celsius(212) == 100

    # Celsius to Kelvin
    assert temp.celsius_to_kelvin(0) == 273.15
    assert temp.celsius_to_kelvin(-273.15) == 0

    # Kelvin to Celsius
    assert temp.kelvin_to_celsius(273.15) == 0
    assert temp.kelvin_to_celsius(0) == -273.15

    # Fahrenheit to Kelvin
    assert temp.fahrenheit_to_kelvin(32) == 273.15
    assert temp.fahrenheit_to_kelvin(-459.67) == 0

    # Kelvin to Fahrenheit
    assert round(temp.kelvin_to_fahrenheit(273.15),0) == 32
    assert temp.kelvin_to_fahrenheit(0) == -459.67

    # Celsius to Rankine
    assert round(temp.celsius_to_rankine(0),2) == 491.67
    assert temp.celsius_to_rankine(100) == 671.67

    # Rankine to Celsius
    assert temp.rankine_to_celsius(491.67) == 0
    assert round(temp.rankine_to_celsius(671.67),0) == 100

    # Fahrenheit to Rankine
    assert temp.fahrenheit_to_rankine(32) == 491.67
    assert temp.fahrenheit_to_rankine(-459.67) == 0

    # Rankine to Fahrenheit
    assert temp.rankine_to_fahrenheit(491.67) == 32
    assert temp.rankine_to_fahrenheit(0) == -459.67

    # General conversion tests
    assert round(temp.convert_temperature(0, temp.UNITS.CELSIUS, temp.UNITS.FAHRENHEIT),2) == 32
    assert round(temp.convert_temperature(32, temp.UNITS.FAHRENHEIT, temp.UNITS.CELSIUS),2) == 0

    print("All temperature conversion tests passed!")

if __name__ == "__main__":
    test_temperature_conversions()