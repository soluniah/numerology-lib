import datetime
import math
from typing import List, Optional

from ..interfaces import DivisibleValue, FactorValue, Period


class Numerology:
    YEARS_OF_CYCLE = 9
    NUMBER_OF_PERIODS = 4
    MAX_NUMBER_ALLOWED_IN_FACTOR = 11
    MAX_NUMBER_ALLOWED_IN_ACHIEVEMENTS_OR_CHALLENGE = 10
    MASTER_NUMBERS = (11, 22, 33)
    KARMIC_NUMBERS = (13, 14, 16, 19)

    def __init__(self, date: str, current_year: Optional[int] = None) -> None:
        self.date: datetime.date = datetime.date.fromisoformat(date)
        self.day: int = self.date.day
        self.month: int = self.date.month
        self.year: int = self.date.year
        self.current_year: int = current_year if current_year is not None else datetime.date.today().year

    def get_soul_number(self) -> FactorValue:
        """Reduced value of the birth day."""
        return self._sum_until_less_or_equal_eleven(self.day)

    def get_karma_number(self) -> FactorValue:
        """Reduced value of the birth month."""
        return self._sum_until_less_or_equal_eleven(self.month)

    def get_gift_number(self) -> FactorValue:
        """Reduced value of the last two digits of the birth year."""
        return self._sum_until_less_or_equal_eleven(self.year % 100)

    def get_destiny_number(self) -> FactorValue:
        """Reduced value of the sum of the birth year digits."""
        return self._sum_until_less_or_equal_eleven(self._sum_digits(self.year))

    def get_path_number(self) -> FactorValue:
        """Reduced value of the sum of day, month and year digits."""
        total = self._sum_digits(self.day) + self._sum_digits(self.month) + self._sum_digits(self.year)
        return self._sum_until_less_or_equal_eleven(total)

    def get_support_number(self) -> int:
        """Reduced sum of the destiny and gift numbers."""
        return self._sum_until_less_or_equal_eleven(
            self.get_destiny_number()["value"] + self.get_gift_number()["value"]
        )["value"]

    def get_obstacle_number(self) -> int:
        """Reduced sum of the soul and karma numbers."""
        return self._sum_until_less_or_equal_eleven(
            self.get_soul_number()["value"] + self.get_karma_number()["value"]
        )["value"]

    def get_personal_year(self) -> int:
        """Reduced personal year based on the configured current_year."""
        current_year_value = self._sum_until_less_or_equal_eleven(self._sum_digits(self.current_year))["value"]
        return self._sum_until_less_or_equal_eleven(
            self.get_soul_number()["value"] + self.get_karma_number()["value"] + current_year_value
        )["value"]

    def get_divisible_numbers(self) -> DivisibleValue:
        """Quotient of soul and karma over destiny when evenly divisible, otherwise 0."""
        soul = self.get_soul_number()["value"]
        karma = self.get_karma_number()["value"]
        destiny = self.get_destiny_number()["value"]

        divisible: DivisibleValue = {"soul": 0, "karma": 0}

        if soul != 0 and destiny != 0:
            max_value = max(soul, destiny)
            min_value = min(soul, destiny)
            divisible["soul"] = max_value // min_value if self._are_divisible(max_value, min_value) else 0

        if karma != 0 and destiny != 0:
            max_value = max(karma, destiny)
            min_value = min(karma, destiny)
            divisible["karma"] = max_value // min_value if self._are_divisible(max_value, min_value) else 0

        return divisible

    def get_achievements_and_challenges(self) -> List[Period]:
        """Four life periods with their achievement and challenge numbers."""
        path = self.get_path_number()["value"]
        achievements = self._get_achievements()
        challenges = self._get_challenges()

        periods: List[Period] = []
        for index, achievement in enumerate(achievements):
            if index == 0:
                period_from = 0
                period_to = self.YEARS_OF_CYCLE * self.NUMBER_OF_PERIODS - path
            elif index == 3:
                period_from = periods[index - 1]["to"]
                period_to = math.inf
            else:
                period_from = periods[index - 1]["to"]
                period_to = period_from + self.YEARS_OF_CYCLE

            period: Period = {
                "from": period_from,
                "to": period_to,
                "achievement": achievement,
                "challenge": challenges[index],
            }
            periods.append(period)

        return periods

    # Private helpers

    def _sum_until_less_or_equal_eleven(self, num: int, master: int = 0, karmic: int = 0) -> FactorValue:
        """Reduce a number to at most 11, preserving any master or karmic number encountered."""
        while num > self.MAX_NUMBER_ALLOWED_IN_FACTOR:
            if num in self.MASTER_NUMBERS:
                master = num
            if num in self.KARMIC_NUMBERS:
                karmic = num
            num = self._sum_digits(num)

        value_factor: FactorValue = {"master": master, "value": num, "karmic": karmic}
        if num in self.MASTER_NUMBERS:
            value_factor["master"] = num
        if num in self.KARMIC_NUMBERS:
            value_factor["karmic"] = num
        return value_factor

    def _calculate_achievement(self, left: int, right: Optional[int] = None) -> int:
        total = left + (right if right is not None else 0)
        if total < self.MAX_NUMBER_ALLOWED_IN_ACHIEVEMENTS_OR_CHALLENGE or total in self.MASTER_NUMBERS:
            return total
        return self._calculate_achievement(self._sum_digits(total))

    def _calculate_challenge(self, left: int, right: Optional[int] = None) -> int:
        diff = abs(left - (right if right is not None else 0))
        if diff < self.MAX_NUMBER_ALLOWED_IN_ACHIEVEMENTS_OR_CHALLENGE or diff in self.MASTER_NUMBERS:
            return diff
        return self._calculate_challenge(self._sum_digits(diff))

    def _get_achievements(self) -> List[int]:
        soul = self._calculate_achievement(self.get_soul_number()["value"])
        karma = self._calculate_achievement(self.get_karma_number()["value"])
        destiny = self._calculate_achievement(self.get_destiny_number()["value"])
        achievement1 = self._calculate_achievement(karma, soul)
        achievement2 = self._calculate_achievement(soul, destiny)
        achievement3 = self._calculate_achievement(achievement1, achievement2)
        achievement4 = self._calculate_achievement(karma, destiny)
        return [achievement1, achievement2, achievement3, achievement4]

    def _get_challenges(self) -> List[int]:
        soul = self._calculate_challenge(self.get_soul_number()["value"])
        karma = self._calculate_challenge(self.get_karma_number()["value"])
        destiny = self._calculate_challenge(self.get_destiny_number()["value"])
        challenge1 = self._calculate_challenge(karma, soul)
        challenge2 = self._calculate_challenge(soul, destiny)
        challenge3 = self._calculate_challenge(challenge1, challenge2)
        challenge4 = self._calculate_challenge(karma, destiny)
        return [challenge1, challenge2, challenge3, challenge4]

    def _are_divisible(self, num1: int, num2: int) -> bool:
        return num1 % num2 == 0

    def _sum_digits(self, num: int) -> int:
        total = 0
        while num > 0:
            num, remainder = divmod(num, 10)
            total += remainder
        return total
