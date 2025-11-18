from robutils.math.measurements import distance as dist

def test_distance_conversions():
    # Miles to Kilometers
    assert round(dist.convert_distance(1, dist.UNIT.MILE, dist.UNIT.KILOMETER), 5) == 1.60934
    assert round(dist.convert_distance(5, dist.UNIT.MILE, dist.UNIT.KILOMETER), 5) == 8.0467

    # Kilometers to Miles
    assert round(dist.convert_distance(1.60934, dist.UNIT.KILOMETER, dist.UNIT.MILE), 5) == 1
    assert round(dist.convert_distance(8.0467, dist.UNIT.KILOMETER, dist.UNIT.MILE), 5) == 5

    # Feet to Meters
    assert round(dist.convert_distance(3.28084, dist.UNIT.FOOT, dist.UNIT.METER), 5) == 1
    assert round(dist.convert_distance(10, dist.UNIT.FOOT, dist.UNIT.METER), 5) == 3.048

    # Meters to Feet
    assert round(dist.convert_distance(1, dist.UNIT.METER, dist.UNIT.FOOT), 5) == 3.28084
    assert round(dist.convert_distance(3.048, dist.UNIT.METER, dist.UNIT.FOOT), 5) == 10

    print("All distance conversion tests passed!")

if __name__ == "__main__":
    test_distance_conversions()