from dataclasses import dataclass
from typing import List

from .flight import Flight
from .car import Car

from datetime import datetime


@dataclass
class Booking:
    tripId: str
    expirationDate: str
    endDate: str
    startDate: str

    flights: List[Flight]
    cars: List[Car]

    @property
    def expiration_date(self) -> datetime:
        return datetime.strptime(self.expirationDate.replace('Z', 'UTC'), "%Y-%m-%dT%H:%M:%S%Z")

    @property
    def end_date(self) -> datetime:
        return datetime.strptime(self.endDate.replace('Z', 'UTC'), "%Y-%m-%dT%H:%M:%S%Z")

    @property
    def start_date(self) -> datetime:
        return datetime.strptime(self.startDate.replace('Z', 'UTC'), "%Y-%m-%dT%H:%M:%S%Z")
