from string import Template


class RyanairAPIEndpoints:
    __base_api_endpoint: str = 'https://api.ryanair.com/usrprof/v2/'
    __base_www_endpoint: str = 'https://www.ryanair.com/api/orders/v2/'

    LOGIN: str = __base_api_endpoint + 'accountLogin?market=it-it'
    DEVICE_FINGERPRINT: str = __base_api_endpoint + 'accountVerifications/deviceFingerprint?market=it-it'
    LOGGED_IN: str = __base_api_endpoint + 'loggedin/'

    SESSION_TOKEN: Template = Template(__base_api_endpoint + 'accounts/${customerId}/sessionToken')

    PROFILE: Template = Template(__base_api_endpoint + 'customers/${customerId}/profile')
    GET_ACTIVE_BOOKINGS: Template = Template(__base_www_endpoint + 'orders/${customerId}?active=true&order=ASC')
    GET_NOT_ACTIVE_BOOKINGS: Template = Template(__base_www_endpoint + 'orders/${customerId}?active=false&order=ASC')

    GET_BOOKING_BY_TRIP_ID: Template = Template(__base_www_endpoint + 'orders/${customerId}/trips/${trip_id}')

    DEFAULT_HEADER = {
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        'Connection': 'keep-alive',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept': 'application/json, text/plain, */*'
    }
