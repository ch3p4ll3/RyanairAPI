from dataclasses import dataclass
from typing import List, Union

from .flight import Flight
from .car import Car

from datetime import datetime


@dataclass
class Booking:
    customerId: str
    tripId: str
    expirationDate: Union[str, datetime]
    endDate: Union[str, datetime]
    startDate: Union[str, datetime]

    flights: List[Flight]
    cars: List[Car]
    rooms: List[str]
    events: List[str]

    def __post_init__(self):
        self.expirationDate = datetime.strptime(self.expirationDate.replace('Z', 'UTC'), "%Y-%m-%dT%H:%M:%S%Z")
        self.endDate = datetime.strptime(self.endDate.replace('Z', 'UTC'), "%Y-%m-%dT%H:%M:%S%Z")
        self.startDate = datetime.strptime(self.startDate.replace('Z', 'UTC'), "%Y-%m-%dT%H:%M:%S%Z")
