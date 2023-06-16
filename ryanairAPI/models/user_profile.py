from dataclasses import dataclass
from datetime import datetime


@dataclass
class UserProfile:
    firstName: str
    lastName: str
    dateOfBirth: str
    maskedDateOfBirth: str
    nationalityCountryCode: str
    googlePictureUrl: str
    email: str
    complete: str
    profileProgress: str
    memberSince: str

    @property
    def date_of_birth(self) -> datetime:
        return datetime.strptime(self.dateOfBirth, "%Y-%m-%d")

    @property
    def member_since(self) -> datetime:
        return datetime.strptime(self.memberSince.replace('Z', 'UTC'), "%Y-%m-%dT%H:%M:%S%Z")
