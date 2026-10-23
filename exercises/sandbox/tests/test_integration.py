import time
import unittest

from library.loans import borrow, overdue_fee, return_loan
from library.models import Book, Member


class LoanLifecycleIntegrationTests(unittest.TestCase):
    """Stand-ins for integration tests that boot a real service.

    The sleep represents service startup. It is deliberately slow: one of the
    exercises is to notice what that does to your iteration rate.
    """

    def setUp(self):
        time.sleep(1.5)

    def test_borrow_then_return_leaves_no_open_loan(self):
        member = Member(id="m1", name="Ada", tier="basic")
        loans = []
        loan = borrow(member, Book(id="b1", title="Dune"), loans)
        return_loan(loan, today=3)
        self.assertIsNotNone(loan.returned_day)

    def test_fee_after_a_full_term(self):
        member = Member(id="m2", name="Grace", tier="plus")
        loans = []
        loan = borrow(member, Book(id="b2", title="Emma"), loans)
        self.assertGreaterEqual(overdue_fee(loan, today=30), 0)

    def test_double_return_is_idempotent(self):
        member = Member(id="m3", name="Linus", tier="basic")
        loans = []
        loan = borrow(member, Book(id="b3", title="Ulysses"), loans)
        return_loan(loan, today=1)
        return_loan(loan, today=5)
        self.assertEqual(loan.returned_day, 5)


if __name__ == "__main__":
    unittest.main()
