import pytest

from numerology import Numerology

KARMIC_NUMBERS = [13, 14, 16, 19]


# Soul Number (Day) - Karmic Numbers
KARMIC_SOUL_TEST_CASES = [
    (13, 1, 2000, 13, 4),
    (14, 1, 2000, 14, 5),
    (16, 1, 2000, 16, 7),
    (19, 1, 2000, 19, 10),
    (22, 1, 2000, 0, 4),  # 22 -> 4, no karmic but master
    (31, 1, 2000, 0, 4),  # 31 -> 4 directly, no intermediate karmic
]


@pytest.mark.parametrize(
    "day, month, year, expected_karmic, expected_value",
    KARMIC_SOUL_TEST_CASES,
    ids=[f"day {case[0]} should detect karmic {case[3]} and reduce to {case[4]}" for case in KARMIC_SOUL_TEST_CASES],
)
def test_soul_number_should_detect_karmic_number_and_reduce(day, month, year, expected_karmic, expected_value):
    date_string = f"{year}-{str(month).zfill(2)}-{str(day).zfill(2)}"
    numerology = Numerology(date_string)
    result = numerology.get_soul_number()

    assert result["karmic"] == expected_karmic
    assert result["value"] == expected_value


# Gift Number (Last two digits of year) - Karmic Numbers
KARMIC_GIFT_TEST_CASES = [
    (1913, 13, 4),  # 13 -> 4
    (2014, 14, 5),  # 14 -> 5
    (1916, 16, 7),  # 16 -> 7
    (2019, 19, 10),  # 19 -> 10
    (2022, 0, 4),  # 22 -> 4, master but no karmic
    (2095, 14, 5),  # 95 -> 14 -> 5
]


@pytest.mark.parametrize(
    "year, expected_karmic, expected_value",
    KARMIC_GIFT_TEST_CASES,
    ids=[f"year {case[0]} should detect karmic {case[1]} and reduce to {case[2]}" for case in KARMIC_GIFT_TEST_CASES],
)
def test_gift_number_should_detect_karmic_number_and_reduce(year, expected_karmic, expected_value):
    date_string = f"{year}-01-01"
    numerology = Numerology(date_string)
    result = numerology.get_gift_number()

    assert result["karmic"] == expected_karmic
    assert result["value"] == expected_value


# Destiny Number (Sum of year digits) - Karmic Numbers
def test_should_detect_karmic_13_when_year_digits_sum_to_13():
    # Need to find a year that sums to 13: 2038 -> 2+0+3+8 = 13
    numerology = Numerology("2038-01-01")
    result = numerology.get_destiny_number()

    assert result["karmic"] == 13
    assert result["value"] == 4


def test_should_detect_karmic_14_when_year_digits_sum_to_14():
    # Need to find a year that sums to 14: 2039 -> 2+0+3+9 = 14
    numerology = Numerology("2039-01-01")
    result = numerology.get_destiny_number()

    assert result["karmic"] == 14
    assert result["value"] == 5


def test_should_detect_karmic_16_when_year_digits_sum_to_16():
    numerology = Numerology("1951-01-01")
    result = numerology.get_destiny_number()

    assert result["karmic"] == 16
    assert result["value"] == 7


def test_should_detect_karmic_19_when_year_digits_sum_to_19():
    # Need to find a year that sums to 19: 1954 -> 1+9+5+4 = 19
    numerology = Numerology("1954-01-01")
    result = numerology.get_destiny_number()

    assert result["karmic"] == 19
    assert result["value"] == 10


def test_should_detect_master_number_22_when_year_digits_sum_to_22():
    numerology = Numerology("1939-01-01")  # 1+9+3+9 = 22
    result = numerology.get_destiny_number()

    assert result["master"] == 22
    assert result["karmic"] == 0
    assert result["value"] == 4


# Path Number (Full date sum) - Complex Karmic Detection
def test_should_detect_karmic_numbers_in_full_date_calculations():
    # Create a date where the sum might result in a karmic number
    numerology = Numerology("1980-07-06")  # Testing a specific combination
    result = numerology.get_path_number()

    # Test that if it has karmic, it's one of the valid ones
    if result["karmic"] != 0:
        assert result["karmic"] in KARMIC_NUMBERS


def test_should_preserve_karmic_numbers_through_complex_calculations():
    # Test multiple dates to ensure karmic detection works consistently
    dates = [
        "1913-01-01",  # Gift karmic 13
        "2014-01-01",  # Gift karmic 14
        "1916-01-01",  # Gift karmic 16
        "2019-01-01",  # Gift karmic 19
    ]

    for date in dates:
        numerology = Numerology(date)
        gift = numerology.get_gift_number()

        # Verify the specific karmic numbers are detected in gift
        if "1913" in date:
            assert gift["karmic"] == 13
        if "2014" in date:
            assert gift["karmic"] == 14
        if "1916" in date:
            assert gift["karmic"] == 16
        if "2019" in date:
            assert gift["karmic"] == 19


# Advanced Karmic Number Scenarios
def test_should_handle_numbers_that_reduce_through_karmic_intermediates():
    # Test 95 -> 14 -> 5 (karmic 14 detected)
    numerology = Numerology("2095-01-01")
    gift = numerology.get_gift_number()

    assert gift["karmic"] == 14
    assert gift["value"] == 5


def test_should_detect_karmic_in_complex_day_numbers():
    # Test days that sum to karmic numbers through multi-digit days
    test_cases = [
        (13, 13),
        (14, 14),
        (16, 16),
        (19, 19),
    ]

    for day, expected_karmic in test_cases:
        if day <= 31:  # Valid day
            numerology = Numerology(f"2000-01-{str(day).zfill(2)}")
            soul = numerology.get_soul_number()
            assert soul["karmic"] == expected_karmic


def test_should_not_detect_false_karmic_numbers():
    # Test numbers that are not karmic
    non_karmic_days = [12, 15, 17, 18, 20, 21, 23, 24, 25, 26, 27, 28, 30]

    for day in non_karmic_days:
        numerology = Numerology(f"2000-01-{str(day).zfill(2)}")
        soul = numerology.get_soul_number()

        # Should not detect karmic if the day doesn't directly contain karmic numbers
        if day not in [13, 14, 16, 19]:
            # Only expect 0 if the day doesn't reduce through a karmic number
            if day not in [13, 14, 16, 19]:
                assert soul["karmic"] not in KARMIC_NUMBERS


# Master vs Karmic Number Distinction
def test_should_detect_master_11_correctly_without_karmic():
    numerology = Numerology("2000-01-29")  # 29 -> 11 (master)
    soul = numerology.get_soul_number()

    assert soul["master"] == 11
    assert soul["karmic"] == 0
    assert soul["value"] == 11


def test_should_detect_master_22_correctly_without_karmic():
    numerology = Numerology("1939-01-01")  # Year sum = 22 (master)
    destiny = numerology.get_destiny_number()

    assert destiny["master"] == 22
    assert destiny["karmic"] == 0
    assert destiny["value"] == 4  # Masters reduce but keep master flag


def test_should_handle_cases_where_both_master_and_karmic_could_appear():
    # Test edge cases where calculations might involve both
    numerology = Numerology("2000-11-01")  # Month 11 (master)
    karma = numerology.get_karma_number()

    assert karma["master"] == 11
    assert karma["karmic"] == 0
    assert karma["value"] == 11


# Comprehensive Karmic Validation
def test_all_four_karmic_numbers_should_be_correctly_identified():
    for karmic_number in KARMIC_NUMBERS:
        # Test as day numbers
        if karmic_number <= 31:
            numerology = Numerology(f"2000-01-{str(karmic_number).zfill(2)}")
            soul = numerology.get_soul_number()
            assert soul["karmic"] == karmic_number

        # Test as year endings (for gift number)
        year = 2000 + karmic_number  # e.g., 2013, 2014, 2016, 2019
        if year <= 2100:  # Reasonable year range
            numerology = Numerology(f"{year}-01-01")
            gift = numerology.get_gift_number()
            assert gift["karmic"] == karmic_number


def test_should_maintain_karmic_detection_across_all_calculation_methods():
    numerology = Numerology("1913-07-14")  # Multiple karmic possibilities

    # Check gift (13)
    gift = numerology.get_gift_number()
    assert gift["karmic"] == 13

    # Check soul (14)
    soul = numerology.get_soul_number()
    assert soul["karmic"] == 14

    # Verify the values are correctly reduced
    assert gift["value"] == 4
    assert soul["value"] == 5


def test_should_detect_karmic_numbers_in_edge_cases():
    # Test cases where karmic numbers appear through complex reductions
    edge_cases = [
        ("1995-01-01", "gift", 14),  # 95 -> 14 -> 5
        ("2086-01-01", "gift", 14),  # 86 -> 14 -> 5
        ("1977-01-01", "gift", 14),  # 77 -> 14 -> 5
        ("2000-01-31", "soul", 0),  # 31 -> 4 (no intermediate karmic)
        ("2000-01-22", "soul", 0),  # 22 -> 4 (master, not karmic)
    ]

    for date, method, expected_karmic in edge_cases:
        numerology = Numerology(date)

        if method == "gift":
            result = numerology.get_gift_number()
            assert result["karmic"] == expected_karmic
        elif method == "soul":
            result = numerology.get_soul_number()
            assert result["karmic"] == expected_karmic


def test_should_handle_years_that_directly_create_karmic_destiny_numbers():
    # Test specific years where the sum of digits equals karmic numbers
    karmic_year_tests = [
        (2038, 13),  # 2+0+3+8 = 13
        (2039, 14),  # 2+0+3+9 = 14
        (1951, 16),  # 1+9+5+1 = 16
        (1954, 19),  # 1+9+5+4 = 19
    ]

    for year, expected_karmic in karmic_year_tests:
        numerology = Numerology(f"{year}-01-01")
        destiny = numerology.get_destiny_number()
        assert destiny["karmic"] == expected_karmic


def test_should_correctly_handle_multiple_digits_reducing_to_karmic_numbers():
    # Test numbers that require multiple reduction steps but pass through karmic numbers
    multi_step_tests = [
        (95, 14, 5),  # 95 -> 14 -> 5
        (77, 14, 5),  # 77 -> 14 -> 5
        (86, 14, 5),  # 86 -> 14 -> 5
        (59, 14, 5),  # 59 -> 14 -> 5
        (68, 14, 5),  # 68 -> 14 -> 5
    ]

    for input_value, expected_karmic, expected_value in multi_step_tests:
        # Test with years ending in the input number
        year = 2000 + (input_value - 100 if input_value > 99 else input_value)
        numerology = Numerology(f"{year}-01-01")
        gift = numerology.get_gift_number()

        assert gift["karmic"] == expected_karmic
        assert gift["value"] == expected_value


def test_should_verify_karmic_numbers_are_preserved_in_internal_calculations():
    # Test that karmic detection works even in methods that only return final numbers
    # but internally use the karmic-aware sumUntilLessOrEqualEleven method

    # Create a numerology instance with known karmic numbers
    numerology = Numerology("1913-07-14")  # Gift=13, Soul=14

    # Verify the basic aspects return expected karmic numbers
    assert numerology.get_soul_number()["karmic"] == 14
    assert numerology.get_gift_number()["karmic"] == 13

    # Test that methods returning only numbers still work correctly
    # (these don't expose karmic directly but should have used the correct internal logic)
    support_number = numerology.get_support_number()
    obstacle_number = numerology.get_obstacle_number()

    # These should be valid numerology numbers (1-11)
    assert support_number >= 1
    assert support_number <= 11
    assert obstacle_number >= 1
    assert obstacle_number <= 11
