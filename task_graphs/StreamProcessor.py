"""A StreamProcessor module used to build stream objects and exceptions."""
from typing import List


class StreamException(Exception):
    pass


class Stream:
    """A stream class providing validation for new lines of text before processing."""

    def __init__(self, lines: List[str]):
        if lines is None or not isinstance(lines, list):
            raise StreamException('Invalid data passed in to stdin.')

        self.lines = lines
