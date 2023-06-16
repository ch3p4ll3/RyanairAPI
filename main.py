from os import getenv

from ryanairAPI import RyanairApi

a = RyanairApi()
a.login(getenv('RYANAIR_EMAIL'), getenv('RYANAIR_PASSWORD'))

print(a.get_user_profile())
