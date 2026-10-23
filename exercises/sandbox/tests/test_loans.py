import unittest

from library.loans import borrow, overdue_fee, paginate
from library.models import Book, Loan, Member


class OverdueFeeTests(unittest.TestCase):
    def test_not_overdue_is_free(self):
        loan = Loan(member_id="m1", book_id="b1", due_day=10)
        self.assertEqual(overdue_fee(loan, today=10), 0)

    def test_overdue_costs_money(self):
        loan = Loan(member_id="m1", book_id="b1", due_day=10)
        self.assertGreater(overdue_fee(loan, today=20), 0)


class BorrowTests(unittest.TestCase):
    def test_borrow_creates_an_open_loan(self):
        member = Member(id="m1", name="Ada", tier="plus")
        loans = []
        borrow(member, Book(id="b1", title="Dune"), loans)
        self.assertEqual(len(loans), 1)
        self.assertIsNone(loans[0].returned_day)


class PaginationTests(unittest.TestCase):
    def test_first_page_returns_ten_items(self):
        items = list(range(1, 26))
        self.assertEqual(paginate(items, page=0, size=10), list(range(1, 11)))


if __name__ == "__main__":
    unittest.main()
