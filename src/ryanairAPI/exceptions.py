from requests.models import Response


class UnableToFindMFAToken(Exception):
    def __init__(self, response: Response):
        self.message = f"Unable to find Mfa Token inside request. Response message: {response.json()}"
        super(UnableToFindMFAToken, self).__init__(self.message)


class UnableToLogin(Exception):
    def __init__(self, response: Response):
        self.message = f"Unable to login. Response message: {response.text}"
        super(UnableToLogin, self).__init__(self.message)


class UnableToFetchUserProfile(Exception):
    def __init__(self, response: Response):
        self.message = f"Unable to fetch user profile. Response message: {response.text}"
        super(UnableToFetchUserProfile, self).__init__(self.message)


class UnableToFetchUpcomingBookings(Exception):
    def __init__(self, response: Response):
        self.message = f"Unable to fetch upcoming bookings. Response message: {response.text}"
        super(UnableToFetchUpcomingBookings, self).__init__(self.message)
