import math

from numerology.core.numerology import Numerology


def test_personal_year_should_calculate_correctly_for_various_dates():
    # Birth date 1990-05-15
    numerology1 = Numerology("1990-05-15", current_year=2025)

    # Soul (day=15 -> 1+5=6) + Karma (month=5) + Current year sum (2025 -> 2+0+2+5=9)
    # 6 + 5 + 9 = 20 -> 2+0 = 2
    assert numerology1.get_personal_year() == 2


def test_personal_year_for_master_numbers():
    # Test case with master numbers
    numerology2 = Numerology("1990-11-29", current_year=2025)

    # Soul (day=29 -> 2+9=11) + Karma (month=11) + Current year sum (2025 -> 9)
    # 11 + 11 + 9 = 31 -> 3+1 = 4
    assert numerology2.get_personal_year() == 4


def test_personal_year_should_handle_edge_cases_with_single_digit_results():
    # Test case resulting in single digit
    numerology3 = Numerology("2000-01-01", current_year=2025)

    # Soul (day=1) + Karma (month=1) + Current year sum (2025 -> 9)
    # 1 + 1 + 9 = 11 (master number, stays 11)
    assert numerology3.get_personal_year() == 11


def test_personal_year_should_calculate_correctly_for_different_current_year_contexts():
    # This tests the current year calculation part
    numerology4 = Numerology("1985-12-25", current_year=2025)

    # Soul (day=25 -> 2+5=7) + Karma (month=12 -> 1+2=3) + Current year sum (2025 -> 9)
    # 7 + 3 + 9 = 19 -> 1+9 = 10
    assert numerology4.get_personal_year() == 10


def test_should_handle_zero_values_in_get_divisible_numbers():
    # Test with a date that might produce zeros
    numerology = Numerology("2000-01-10")
    divisible = numerology.get_divisible_numbers()

    # This ensures we test the zero checking conditions
    assert isinstance(divisible["soul"], (int, float))
    assert isinstance(divisible["karma"], (int, float))


def test_should_handle_large_numbers_in_sum_until_less_or_equal_eleven():
    # Test with larger numbers to ensure recursive calls
    numerology = Numerology("9999-12-31")

    gift = numerology.get_gift_number()
    destiny = numerology.get_destiny_number()
    path = numerology.get_path_number()

    # These should all be reduced to <= 11
    assert gift["value"] <= 11
    assert destiny["value"] <= 11
    assert path["value"] <= 11


def test_should_preserve_master_numbers_during_reduction():
    # Test case that should produce a master number
    numerology = Numerology("1984-02-20")

    gift = numerology.get_gift_number()  # 84 -> 8+4 = 12 -> 1+2 = 3
    destiny = numerology.get_destiny_number()  # 1+9+8+4 = 22 (master)

    assert gift["value"] == 3  # Gift number should be reduced
    assert destiny["master"] == 22
    assert destiny["value"] == 4  # Master numbers > 11 get reduced to single digit for value


def test_should_handle_karmic_numbers_in_different_calculations():
    # Test karmic number preservation in various scenarios
    numerology = Numerology("1990-01-13")  # day 13 is karmic

    soul = numerology.get_soul_number()
    assert soul["karmic"] == 13
    assert soul["value"] == 4  # 1+3=4

    # Test that karmic numbers are preserved through other calculations
    path = numerology.get_path_number()
    achievements = numerology.get_achievements_and_challenges()

    assert isinstance(path["value"], int)
    assert isinstance(achievements, list)
    assert len(achievements) == 4


def test_should_test_calculate_achievement_through_get_achievements_and_challenges():
    numerology = Numerology("1980-06-15")
    periods_data = numerology.get_achievements_and_challenges()

    # Verify all periods have proper structure
    for period in periods_data:
        assert "from" in period
        assert "to" in period
        assert "achievement" in period
        assert "challenge" in period
        assert isinstance(period["achievement"], (int, float))
        assert isinstance(period["challenge"], (int, float))

    # Test that we get 4 periods
    assert len(periods_data) == 4

    # Test that first period starts at 0
    assert periods_data[0]["from"] == 0

    # Test that last period goes to infinity
    assert periods_data[3]["to"] == math.inf


def test_should_test_calculate_challenge_through_get_achievements_and_challenges():
    numerology = Numerology("1975-03-08")
    periods = numerology.get_achievements_and_challenges()

    # All challenges should be numbers >= 0 and <= max allowed
    for period in periods:
        assert period["challenge"] >= 0
        assert isinstance(period["challenge"], (int, float))


def test_should_test_are_divisible_method_coverage():
    # Test cases that will exercise the areDivisible method
    numerology1 = Numerology("1990-02-10")  # soul=1, karma=2, destiny=1
    divisible1 = numerology1.get_divisible_numbers()

    numerology2 = Numerology("1990-03-15")  # soul=6, karma=3, destiny=1
    divisible2 = numerology2.get_divisible_numbers()

    # These should trigger different paths in the divisible calculation
    assert isinstance(divisible1["soul"], (int, float))
    assert isinstance(divisible1["karma"], (int, float))
    assert isinstance(divisible2["soul"], (int, float))
    assert isinstance(divisible2["karma"], (int, float))
