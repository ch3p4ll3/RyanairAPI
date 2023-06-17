from string import Template


class RyanairAPIEndpoints:
    __base_endpoint: str = 'https://api.ryanair.com/usrprof/v2/'

    LOGIN: str = __base_endpoint + 'accountLogin?market=it-it'
    DEVICE_FINGERPRINT: str = __base_endpoint + 'accountVerifications/deviceFingerprint?market=it-it'
    LOGGED_IN: str = __base_endpoint + 'loggedin/'

    SESSION_TOKEN: Template = Template(__base_endpoint + 'accounts/{$customerId}/sessionToken')

    PROFILE: Template = Template(__base_endpoint + 'customers/{$customerId}/profile')
    GET_ACTIVE_BOOKINGS: Template = Template(__base_endpoint + 'orders/{$customerId}?active=true&order=ASC')
    GET_NOT_ACTIVE_BOOKINGS: Template = Template(__base_endpoint + 'orders/{$customerId}?active=false&order=ASC')

    DEFAULT_HEADER = {
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        'Connection': 'keep-alive',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept': 'application/json, text/plain, */*'
    }
