from string import Template


class RyanairAPIEndpoints:
    __base_endpoint = 'https://api.ryanair.com/usrprof/v2/'

    login = __base_endpoint + 'accountLogin?market=it-it'
    device_fingerprint = __base_endpoint + 'accountVerifications/deviceFingerprint?market=it-it'
    logged_in = __base_endpoint + 'loggedin/'

    session_token = Template(__base_endpoint + 'accounts/{$customerId}/sessionToken')

    profile = Template(__base_endpoint + 'customers/{$customerId}/profile')
    get_active_bookings = Template(__base_endpoint + 'orders/{$customerId}?active=true&order=ASC')
    get_not_active_bookings = Template(__base_endpoint + 'orders/{$customerId}?active=false&order=ASC')

    default_header = {
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    }
