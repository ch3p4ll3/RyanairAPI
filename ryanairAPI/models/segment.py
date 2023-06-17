from dataclasses import dataclass
from typing import Union

from datetime import datetime


@dataclass
class Segment:
    departureTime: Union[str, datetime]
    arrivalTime: Union[str, datetime]
    destination: str
    origin: str
    flightNumber: str

    def __post_init__(self):
        self.departureTime = datetime.strptime(self.departureTime.replace('Z', 'UTC'), "%Y-%m-%dT%H:%M:%S%Z")
        self.arrivalTime = datetime.strptime(self.arrivalTime.replace('Z', 'UTC'), "%Y-%m-%dT%H:%M:%S%Z")
