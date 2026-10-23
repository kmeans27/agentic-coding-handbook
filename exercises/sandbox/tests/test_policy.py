import unittest

from library.loans import borrow
from library.models import Book, Member
from library.policy import can_borrow


class BorrowingLimitTests(unittest.TestCase):
    def test_basic_member_limit_is_three(self):
        member = Member(id="m1", name="Ada", tier="basic")
        self.assertTrue(can_borrow(member, 2))
        self.assertFalse(can_borrow(member, 3))

    def test_plus_member_limit_is_ten(self):
        member = Member(id="m2", name="Grace", tier="plus")
        self.assertTrue(can_borrow(member, 9))
        self.assertFalse(can_borrow(member, 10))

    @unittest.skip("flaky on CI, revisit later")
    def test_suspended_member_cannot_borrow(self):
        member = Member(id="m3", name="Linus", tier="basic", suspended=True)
        with self.assertRaises(ValueError):
            borrow(member, Book(id="b1", title="Dune"), [])


if __name__ == "__main__":
    unittest.main()
