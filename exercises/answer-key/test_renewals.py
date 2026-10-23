import unittest

from library.loans import MAX_RENEWALS, RenewalError, renew
from library.models import Book, Loan, Member


class RenewalTests(unittest.TestCase):
    def setUp(self):
        self.member = Member(id="m1", name="Ada", tier="plus")
        self.book = Book(id="b1", title="Dune")
        self.loan = Loan(member_id="m1", book_id="b1", due_day=14)

    def test_renewal_extends_from_the_current_due_day(self):
        renew(self.loan, self.member, today=10)
        self.assertEqual(self.loan.due_day, 28)
        self.assertEqual(self.loan.renewals, 1)

    def test_two_renewals_are_allowed(self):
        renew(self.loan, self.member, today=10)
        renew(self.loan, self.member, today=20)
        self.assertEqual(self.loan.due_day, 42)
        self.assertEqual(self.loan.renewals, 2)

    def test_third_renewal_is_rejected(self):
        renew(self.loan, self.member, today=10)
        renew(self.loan, self.member, today=20)
        with self.assertRaises(RenewalError):
            renew(self.loan, self.member, today=30)
        self.assertEqual(self.loan.due_day, 42)

    def test_overdue_loan_cannot_be_renewed(self):
        with self.assertRaises(RenewalError):
            renew(self.loan, self.member, today=15)
        self.assertEqual(self.loan.due_day, 14)

    def test_suspended_member_cannot_renew(self):
        self.member.suspended = True
        with self.assertRaises(RenewalError):
            renew(self.loan, self.member, today=10)

    def test_returned_loan_cannot_be_renewed(self):
        self.loan.returned_day = 12
        with self.assertRaises(RenewalError):
            renew(self.loan, self.member, today=20)


if __name__ == "__main__":
    unittest.main()
