from dataclasses import dataclass
from .segment import Segment
from typing import List


@dataclass
class Journey:
    segments: List[Segment]
