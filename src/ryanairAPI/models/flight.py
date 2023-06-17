from dataclasses import dataclass
from typing import List, Union
from .journey import Journey

from datetime import datetime


@dataclass
class Flight:
    origin: str
    destination: str
    departureDate: Union[str, datetime]
    arrivalDate: Union[str, datetime]
    pnr: str

    journeys: List[Journey]

    addOns: str
    bookingId: str

    def __post_init__(self):
        self.departureDate = datetime.strptime(self.departureDate.replace('Z', 'UTC'), "%Y-%m-%dT%H:%M:%S%Z")
        self.arrivalDate = datetime.strptime(self.arrivalDate.replace('Z', 'UTC'), "%Y-%m-%dT%H:%M:%S%Z")
