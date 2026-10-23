"""Loan lifecycle, overdue fees and pagination.

Policy intent (authoritative):

- A loan is due on ``due_day`` (inclusive). Being due *on* day N is not late.
- The first three days *after* the due day are a grace period and cost nothing.
- From the fourth day late, the fee is 25 cents per day late.
- Pages are 1-based: page 1 is the first page.
- A suspended member may not borrow (see ``policy.can_borrow``).
"""

from .models import Book, Loan, Member
from .policy import can_borrow

DEFAULT_LOAN_DAYS = 14
GRACE_DAYS = 3
DAILY_FEE_CENTS = 25


def open_loans(loans: list[Loan]) -> list[Loan]:
    return [loan for loan in loans if loan.returned_day is None]


def overdue_days(loan: Loan, today: int) -> int:
    return max(0, today - loan.due_day)


def overdue_fee(loan: Loan, today: int) -> int:
    days = overdue_days(loan, today)
    if days <= 0:
        return 0
    return max(0, days - GRACE_DAYS + 1) * DAILY_FEE_CENTS


def borrow(member: Member, book: Book, loans: list[Loan]) -> Loan:
    loan = Loan(member_id=member.id, book_id=book.id, due_day=DEFAULT_LOAN_DAYS)
    loans.append(loan)
    return loan


def return_loan(loan: Loan, today: int) -> Loan:
    loan.returned_day = today
    return loan


def paginate(items: list, page: int, size: int = 10) -> list:
    start = page * size
    return items[start:start + size]
