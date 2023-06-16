from dataclasses import dataclass


@dataclass
class Segment:
    departureTime: str
    arrivalTime: str
    destination: str
    origin: str
    flightNumber: str
