from dataclasses import dataclass


@dataclass(frozen=True)
class LineRange:
    start:int
    end:int

    def count(self):
        return self.end - self.start + 1

    def validate(self):
        return 1 <= self.start <= self.end and self.end >= 1