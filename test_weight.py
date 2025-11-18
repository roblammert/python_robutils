from robutils.math.measurements import weight

def test_convert_weight():
    # Test conversion from pounds to kilograms
    pounds = 10
    expected_kg = 4.53592  # 10 pounds in kg
    converted_kg = weight.convert_weight(pounds, weight.UNIT.POUND, weight.UNIT.KILOGRAM)
    assert abs(converted_kg - expected_kg) < 1e-5

    # Test conversion from kilograms to pounds
    kg = 5
    expected_pounds = 11.0231  # 5 kg in pounds
    converted_pounds = weight.convert_weight(kg, weight.UNIT.KILOGRAM, weight.UNIT.POUND)
    assert round(abs(converted_pounds - expected_pounds),4) < 1e-5

    # Test conversion from ounces to grams
    ounces = 16
    expected_grams = 453.592  # 16 ounces in grams
    converted_grams = weight.convert_weight(ounces, weight.UNIT.OUNCE, weight.UNIT.GRAM)
    assert abs(converted_grams - expected_grams) < 1e-3

    # Test conversion from grams to ounces
    grams = 1000
    expected_ounces = 35.27396  # 1000 grams in ounces
    converted_ounces = weight.convert_weight(grams, weight.UNIT.GRAM, weight.UNIT.OUNCE)
    assert abs(converted_ounces - expected_ounces) < 1e-5

   # Test conversion from slugs to kilograms
    slugs = 2
    expected_kg = 29.1878  # 2 slugs in kg
    converted_kg = weight.convert_weight(slugs, weight.UNIT.SLUG, weight.UNIT.KILOGRAM)
    assert abs(converted_kg - expected_kg) < 1e-4

    # Test conversion from tonnes to pounds
    tonnes = 3
    expected_pounds = 6613.87  # 3 tonnes in pounds
    converted_pounds = weight.convert_weight(tonnes, weight.UNIT.TONNE, weight.UNIT.POUND)
    assert abs(converted_pounds - expected_pounds) < 1e-2
 
    print("All weight conversion tests passed.")

if __name__ == "__main__":
    test_convert_weight()
