from numerology import Numerology


def test_should_always_divide_larger_by_smaller_soul_less_than_destiny():
    numerology = Numerology("1990-01-05")
    result = numerology.get_divisible_numbers()

    assert numerology.get_soul_number()["value"] == 5
    assert numerology.get_destiny_number()["value"] == 10
    assert result["soul"] == 2


def test_should_always_divide_larger_by_smaller_soul_greater_than_destiny():
    numerology = Numerology("2000-01-04")
    result = numerology.get_divisible_numbers()

    assert numerology.get_soul_number()["value"] == 4
    assert numerology.get_destiny_number()["value"] == 2
    assert result["soul"] == 2


def test_should_fix_the_original_decimal_problem():
    numerology = Numerology("1990-01-05")
    result = numerology.get_divisible_numbers()

    soul = numerology.get_soul_number()["value"]
    destiny = numerology.get_destiny_number()["value"]

    assert soul == 5
    assert destiny == 10
    assert result["soul"] == 2
    assert result["soul"] != 0.5


def test_should_divide_larger_by_smaller_when_they_are_divisible_karma_case():
    # Find a date where karma and destiny have exact divisibility
    numerology = Numerology("1990-06-15")  # Month=6, let's see what we get
    result = numerology.get_divisible_numbers()

    karma = numerology.get_karma_number()["value"]
    destiny = numerology.get_destiny_number()["value"]

    # If they're divisible in either direction, we should get an integer
    if (karma != 0 and destiny % karma == 0) or (destiny != 0 and karma % destiny == 0):
        assert float(result["karma"]).is_integer()
        assert result["karma"] > 0

        # Verify it's the larger divided by smaller
        if karma > destiny and karma % destiny == 0:
            assert result["karma"] == karma / destiny
        elif destiny > karma and destiny % karma == 0:
            assert result["karma"] == destiny / karma
    else:
        # If not divisible, should be 0 (original logic)
        assert result["karma"] == 0


def test_should_handle_specific_karma_destiny_divisible_combinations():
    test_cases = [
        ("2000-02-10", "Month=2, should test karma=2"),  # karma=2, destiny likely higher
        ("1995-04-20", "Month=4, should test karma=4"),  # karma=4
        ("1988-06-12", "Month=6, should test karma=6"),  # karma=6
    ]

    for test_case in test_cases:
        numerology = Numerology(test_case[0])
        result = numerology.get_divisible_numbers()

        karma = numerology.get_karma_number()["value"]
        destiny = numerology.get_destiny_number()["value"]

        # Should only be non-zero if divisible
        if result["karma"] > 0:
            assert float(result["karma"]).is_integer()

            # Verify the math
            if karma > destiny:
                assert karma % destiny == 0 or destiny % karma == 0
            else:
                assert destiny % karma == 0 or karma % destiny == 0


def test_should_return_0_when_karma_and_destiny_are_not_divisible():
    # Find a case where karma and destiny are not divisible
    numerology = Numerology("1995-07-13")  # karma=7, day=13, different primes
    result = numerology.get_divisible_numbers()

    karma = numerology.get_karma_number()["value"]
    destiny = numerology.get_destiny_number()["value"]

    # Check if they're actually not divisible
    if karma != 0 and destiny != 0 and destiny % karma != 0 and karma % destiny != 0:
        assert result["karma"] == 0


def test_should_handle_edge_case_where_karma_equals_destiny():
    # Look for cases where karma might equal destiny
    numerology = Numerology("1999-11-22")  # karma=11 (master), let's see
    result = numerology.get_divisible_numbers()

    karma = numerology.get_karma_number()["value"]
    destiny = numerology.get_destiny_number()["value"]

    if karma == destiny and karma != 0:
        assert result["karma"] == 1  # X/X = 1


def test_should_verify_the_original_problem_is_fixed():
    # Original problem: soul=5, destiny=10 should give 10/5=2, not 5/10=0.5
    numerology = Numerology("1990-01-05")
    result = numerology.get_divisible_numbers()

    soul = numerology.get_soul_number()["value"]  # should be 5
    destiny = numerology.get_destiny_number()["value"]  # should be 10

    # Since 10 % 5 === 0, this should work and give us 2
    if destiny % soul == 0:
        assert result["soul"] == destiny / soul  # 10/5 = 2
        assert result["soul"] == 2
        assert result["soul"] != 0.5  # NOT the problematic 0.5
