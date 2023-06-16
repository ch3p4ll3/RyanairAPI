from dataclasses import dataclass
from typing import List
from .journey import Journey

from datetime import datetime


@dataclass
class Flight:
    origin: str
    destination: str
    departureDate: str
    arrivalDate: str
    pnr: str

    journeys: List[Journey]

    addOns: str
    bookingId: str

    @property
    def departure_date(self) -> datetime:
        return datetime.strptime(self.departureDate.replace('Z', 'UTC'), "%Y-%m-%dT%H:%M:%S%Z")

    @property
    def arrival_date(self) -> datetime:
        return datetime.strptime(self.arrivalDate.replace('Z', 'UTC'), "%Y-%m-%dT%H:%M:%S%Z")
