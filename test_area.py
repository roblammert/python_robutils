from robutils.math.measurements import area as ar

def test_convert_area():
    # Test conversion from square meters to square feet
    assert abs(ar.convert_area(1, ar.UNITS._SQUARE_METER, ar.UNITS._SQUARE_FOOT) - 10.7639) < 0.0001
    # Test conversion from acres to square meters
    assert abs(ar.convert_area(1, ar.UNITS._ACRE, ar.UNITS._SQUARE_METER) - 4046.86) < 0.01
    # Test conversion from square miles to acres
    assert abs(ar.convert_area(1, ar.UNITS._SQUARE_MILE, ar.UNITS._ACRE) - 640) < 0.01
    # Test conversion from square centimeters to square inches
    assert abs(ar.convert_area(100, ar.UNITS._SQUARE_CENTIMETER, ar.UNITS._SQUARE_INCH) - 15.5000) < 0.0001
def test_calculate_triangle_area():
    # Test area calculation for a triangle with base 10 and height 5
    assert ar.calculate_triangle_area(10, 5) == 25.0
    # Test area calculation for a triangle with base 0 and height 5
    assert ar.calculate_triangle_area(0, 5) == 0.0
    # Test area calculation for a triangle with base 7.5 and height 3.2
    assert abs(ar.calculate_triangle_area(7.5, 3.2) - 12.0) < 0.0001
def test_calculate_circle_area():
    import math
    # Test area calculation for a circle with radius 1
    assert abs(ar.calculate_circle_area(1) - math.pi) < 0.0001
    # Test area calculation for a circle with radius 0
    assert ar.calculate_circle_area(0) == 0.0
    # Test area calculation for a circle with radius 2.5
    assert abs(ar.calculate_circle_area(2.5) - (math.pi * 2.5 ** 2)) < 0.0001

if __name__ == "__main__":
    test_convert_area()
    test_calculate_triangle_area()
    test_calculate_circle_area()
    print("All area tests passed!")