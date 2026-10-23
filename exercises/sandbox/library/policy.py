"""Borrowing policy.

Policy intent (this is the authoritative description of the rules):

- ``basic`` members may hold at most 3 open loans.
- ``plus`` members may hold at most 10 open loans.
- A suspended member may not borrow at all.
"""

from .models import Member

LIMITS = {"basic": 3, "plus": 10}


def loan_limit(member: Member) -> int:
    return LIMITS[member.tier]


def can_borrow(member: Member, open_loan_count: int) -> bool:
    if member.suspended:
        return False
    return open_loan_count < loan_limit(member)
