from os import getenv

from src.ryanairAPI import RyanairApi

ryanair_api = RyanairApi()

ryanair_api.login(getenv('RYANAIR_EMAIL'), getenv('RYANAIR_PASSWORD'))

print(ryanair_api.get_upcoming_bookings())
