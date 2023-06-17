import os.path

import requests
import pickle
import json
import logging

from typing import List

from .exceptions import UnableToFindMFAToken, UnableToLogin, UnableToFetchUserProfile, UnableToFetchUpcomingBookings
from .endpoints import RyanairAPIEndpoints
from .models import UserProfile, Booking, Flight, Segment, Journey


class RyanairApi:
    logging.basicConfig(filename='/dev/null', level=logging.NOTSET)

    __http_session = requests.Session()
    __http_session.headers = RyanairAPIEndpoints.DEFAULT_HEADER

    __customerId = ""
    __authToken = ""
    __sessionToken = ""

    def __init__(self):
        pass

    def login(self, username: str, password: str) -> None:
        self.__import_session()
        self.__standard_login(username, password)

    def __standard_login(self, username, password):
        self.__http_session.get('https://www.ryanair.com/it/it')

        data = json.dumps({'email': username, 'password': password, 'policyAgreed': True})

        response = self.__http_session.post(
            RyanairAPIEndpoints.LOGIN,
            headers=RyanairAPIEndpoints.DEFAULT_HEADER,
            data=data
        )

        if response.status_code == 403:
            response = self.__login_mfa(response)

        if response.status_code != 200:
            logging.error('Impossible to login')
            raise UnableToLogin(response)

        data = response.json()

        self.__customerId = data['customerId']
        self.__authToken = data['token']

        self.__export_session()
        # self.get_session_token()

        logging.debug('User logged in')

    def __login_mfa(self, response) -> requests.Response:
        try:
            additional_data = response.json().get('additionalData', [])
            mfa_token = next(iter(additional_data), {}).get('message')
        except Exception:
            raise UnableToFindMFAToken(response)

        if mfa_token:
            token = input('Insert the token received by email: ')

            data = json.dumps({
                'mfaCode': token,
                'mfaToken': mfa_token
            })

            response = self.__http_session.put(
                RyanairAPIEndpoints.DEVICE_FINGERPRINT,
                headers=RyanairAPIEndpoints.DEFAULT_HEADER,
                data=data
            )

            return response

    def __export_session(self):
        with open('session', 'wb') as f:
            pickle.dump(self.__http_session.cookies, f)

    def __import_session(self):
        if not os.path.exists('./session'):
            return

        with open('session', 'rb') as f:
            self.__http_session.cookies.update(pickle.load(f))

    def get_session_token(self):
        response = self.__http_session.get(
            RyanairAPIEndpoints.SESSION_TOKEN.substitute(customerId=self.__customerId),
            headers=RyanairAPIEndpoints.DEFAULT_HEADER
        )

        if response.status_code != 200:
            raise Exception

        self.__sessionToken = response.json().get('token')

    def get_user_profile(self) -> UserProfile:
        """Return user profile"""
        self.__http_session.headers['X-Auth-Token'] = self.__authToken
        self.__http_session.headers['X-Session-Token'] = self.__sessionToken

        response = self.__http_session.get(
            RyanairAPIEndpoints.PROFILE.substitute(customerId=self.__customerId),
            headers=self.__http_session.headers
        )

        if response.status_code != 200:
            logging.error('Impossible to fetch profile')
            raise UnableToFetchUserProfile(response)

        user = response.json()
        user.pop('title')

        return UserProfile(**user)

    def get_upcoming_bookings(self) -> List[Booking]:
        """Get the list of all upcoming bookings"""
        headers = RyanairAPIEndpoints.DEFAULT_HEADER
        headers.update({
            'X-Auth-Token': self.__authToken
        })

        response = requests.get(
            RyanairAPIEndpoints.GET_ACTIVE_BOOKINGS.substitute(customerId=self.__customerId),
            headers=headers
        )

        if response.status_code != 200:
            logging.error('Impossible to fetch upcoming bookings')
            UnableToFetchUpcomingBookings(response)

        raw_bookings = response.json()
        bookings = []

        for booking in raw_bookings.get('items', []):
            booking.pop('productTypes')

            raw_flights = booking.pop('flights')
            flights = RyanairApi.__parse_flights(raw_flights)
            bookings.append(Booking(flights=flights, **booking))

        return bookings

    @staticmethod
    def __parse_flights(raw_flights: List[dict]) -> List[Flight]:
        flights = []
        journeys = []

        for flight in raw_flights:
            flight.pop('passengers')

            for journey in flight.pop('journeys'):
                segments = []
                for segment in journey.pop('segments'):
                    segments.append(Segment(**segment))
                journeys.append(Journey(segments))

            flights.append(Flight(journeys=journeys, **flight))

        return flights

    def get_all_seats(self):
        bookings = self.get_upcoming_bookings()
        # Display every booking
        for travel in bookings:
            self.infoBooking(travel.tripId)
        return

    def info_booking(self, booking_id: str):
        """ Get and display information about one booking:
        - Print informations about the flights on the booking
        - Print informations about the passengers of the flights
        - Print a guess of the seat it will be allocated to the passengers
        """
        url = 'v4/Booking'
        headers = utils.getHeaders()
        headers.update({
            'Content-Type': 'application/json',
            'Content-Length': '52',
            'X-Auth-Token': self.authToken
        })
        data = {
            'surrogateId': self.customerId,
            'bookingId': bookingId
        }
        response = requests.post(
            self.bookingApiUrl + url,
            headers=headers,
            data=json.dumps(data))

        if response.status_code != 200:
            logging.error('Impossible to fetch bookings')
            print('Impossible to fetch bookings!')
            exit(1)
        result = response.json()

        # Save the received sessionToken
        self.sessionToken = response.headers['X-Session-Token']
        # Get informations about seats for this booking
        seatsList = self.infoSeats()
        if seatsList is False:
            logging.error('Impossible to fetch seats')
            print('Impossible to fetch seats!')
            exit(1)

        # Flight info
        print('Prenotation number: %s (Status of the flight: %s)' % (
            utils.bclr.OKBLUE + result['info']['pnr'] + utils.bclr.ENDC,
            utils.bclr.OKGREEN + result['info']['status'] + utils.bclr.ENDC))
        numberofSeats = len(result['passengers'])
        print ('Number of passengers: %s' % numberofSeats)
        c = 0
        # Print information about passengers
        for passenger in result['passengers']:
            c += 1
            print ('  %i: %s %s' % (
                c,
                utils.bclr.HEADER + passenger['name']['first'],
                passenger['name']['last'] + utils.bclr.ENDC))
        c = 0
        for journey in result['journeys']:

            print ('   [%s] %s -> %s (%s)' % (
                utils.bclr.OKBLUE + journey['flt'] + utils.bclr.ENDC,
                utils.bclr.WARNING + journey['orig'] + utils.bclr.ENDC,
                utils.bclr.WARNING + journey['dest'] + utils.bclr.ENDC,
                utils.parseDate(journey['depart'])))

            if 'reasonCode' in journey['changeInfo'] and \
               journey['changeInfo']['reasonCode'] == 'PassengerCheckedIn':
                print ('   Already checked-in')
            else:
                allocation = self.getSeat(
                    seatsList[c]['unavailableSeats'],
                    numberofSeats)
                if (allocation['status'] == 'error'):
                    print (allocation['message'])
                else:
                    print ('   If you do check-in now, you will have \
seat %s %s' % (
                        utils.bclr.OKGREEN +
                        allocation['seat'] +
                        utils.bclr.ENDC,
                        seats.seatInfo(allocation['seat'])))
            c += 1
        return

    def infoSeats(self):
        """ Show informations about seats for the booking
        - Return also the list of unavailable (already allocated) seats
        """
        url = 'v4/Seat'
        headers = utils.getHeaders()
        headers.update({
            'X-Session-Token': self.sessionToken
        })
        response = requests.get(self.bookingApiUrl + url, headers=headers)
        if response.status_code == 200:
            return response.json()
        return False

    def getSeat(self, unavailable, numberofSeats):
        """ Return the seat that will be allocated during check-in"""
        response = dict()
        if utils.MAXPASSENGERS > numberofSeats:
            response['status'] = 'error'
            response['message'] = '   We are sorry but we currently \
don\'t support seat prediction for flights \
with %s passengers.' % numberofSeats
        else:
            response['status'] = 'ok'
            response['seat'] = seats.getFirstFree(unavailable)

        return response