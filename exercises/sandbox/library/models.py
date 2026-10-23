"""Domain models for the practice library."""

from dataclasses import dataclass


@dataclass
class Member:
    id: str
    name: str
    tier: str = "basic"  # "basic" or "plus"
    suspended: bool = False


@dataclass
class Book:
    id: str
    title: str
    copies: int = 1


@dataclass
class Loan:
    member_id: str
    book_id: str
    due_day: int
    returned_day: int | None = None
