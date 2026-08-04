import pytest

from numerology import Numerology
from tests.resources.dataset import dataset


@pytest.mark.parametrize(
    "date_of_birth, expected_soul, expected_karma, expected_gift, expected_destiny, "
    "expected_path, expected_support, expected_obstacle, expected_divisible, "
    "expected_personal_year, challenge_and_achievements",
    [
        pytest.param(
            str(row["date_of_birth"]),
            row["expected_soul"],
            row["expected_karma"],
            row["expected_gift"],
            row["expected_destiny"],
            row["expected_path"],
            row["expected_support"],
            row["expected_obstacle"],
            row["expected_divisible"],
            row["expected_personal_year"],
            row["challenge_and_achievements"],
            id=f"born {row['date_of_birth']}",
        )
        for row in dataset
    ],
)
def test_numerology(
    date_of_birth,
    expected_soul,
    expected_karma,
    expected_gift,
    expected_destiny,
    expected_path,
    expected_support,
    expected_obstacle,
    expected_divisible,
    expected_personal_year,
    challenge_and_achievements,
):
    numerology = Numerology(date_of_birth)

    assert numerology.get_soul_number() == expected_soul
    assert numerology.get_karma_number() == expected_karma
    assert numerology.get_gift_number() == expected_gift
    assert numerology.get_destiny_number() == expected_destiny
    assert numerology.get_path_number() == expected_path
    assert numerology.get_support_number() == expected_support
    assert numerology.get_obstacle_number() == expected_obstacle
    assert numerology.get_divisible_numbers() == expected_divisible
    assert numerology.get_achievements_and_challenges() == challenge_and_achievements
