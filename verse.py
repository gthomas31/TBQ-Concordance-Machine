from dataclasses import dataclass


@dataclass(frozen=True)
class Verse:
    book: str
    chapter: int
    verse: int
    section: str
    text: str
