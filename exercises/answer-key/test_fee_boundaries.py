import unittest

from library.loans import overdue_fee
from library.models import Loan


class FeeBoundaryTests(unittest.TestCase):
    """Pins the fee table from the policy docstring, not the implementation.

    Due day is 10. The three days after it are free; the fourth costs 25c.
    """

    def setUp(self):
        self.loan = Loan(member_id="m1", book_id="b1", due_day=10)

    def test_whole_table(self):
        expected = {10: 0, 11: 0, 12: 0, 13: 0, 14: 25, 15: 50, 16: 75}
        actual = {today: overdue_fee(self.loan, today) for today in expected}
        self.assertEqual(actual, expected)

    def test_grace_period_is_exactly_three_days(self):
        self.assertEqual(overdue_fee(self.loan, 13), 0)
        self.assertEqual(overdue_fee(self.loan, 14), 25)

    def test_fee_is_linear_after_the_grace_period(self):
        self.assertEqual(
            [overdue_fee(self.loan, 14 + n) for n in range(5)],
            [25, 50, 75, 100, 125],
        )


if __name__ == "__main__":
    unittest.main()
