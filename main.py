from os import getenv

from ryanairAPI import RyanairApi

ryanair_api = RyanairApi()

ryanair_api.login(getenv('RYANAIR_EMAIL'), getenv('RYANAIR_PASSWORD'))

print(ryanair_api.get_booking_by_trip_id('4581de0f-c29a-40e1-8bfe-7c967b216466'))
