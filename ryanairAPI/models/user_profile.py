from dataclasses import dataclass
from datetime import datetime

from re import sub

from typing import Union


@dataclass
class UserProfile:
    firstName: str
    lastName: str
    dateOfBirth: Union[str, datetime]
    maskedDateOfBirth: str
    nationalityCountryCode: str
    googlePictureUrl: str
    email: str
    complete: str
    profileProgress: str
    memberSince: Union[str, datetime]

    def __post_init__(self):
        self.dateOfBirth = datetime.strptime(self.dateOfBirth, "%Y-%m-%d")

        self.memberSince = sub(r'\.\d+Z', 'UTC', self.memberSince)
        self.memberSince = datetime.strptime(self.memberSince.replace('Z', 'UTC'), "%Y-%m-%dT%H:%M:%S%Z")
