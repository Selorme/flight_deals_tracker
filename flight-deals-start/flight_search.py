import os
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

IATA_ENDPOINT = "https://test.api.amadeus.com/v1/reference-data/locations/cities"
FLIGHT_ENDPOINT = "https://test.api.amadeus.com/v2/shopping/flight-offers"
TOKEN_ENDPOINT = "https://test.api.amadeus.com/v1/security/oauth2/token"


class FlightSearch:
    def __init__(self):
        self._api_key = os.environ["AMADEUS_API_KEY"]
        self._api_secret = os.environ["AMADEUS_SECRET"]
        self._token = self._get_new_token()

    def _get_new_token(self):
        header = {'Content-Type': 'application/x-www-form-urlencoded'}
        body = {
            'grant_type': 'client_credentials',
            'client_id': self._api_key,
            'client_secret': self._api_secret
        }
        response = requests.post(url=TOKEN_ENDPOINT, headers=header, data=body)
        if response.status_code == 200:
            token = response.json().get('access_token')
            if token:
                return token
            else:
                print("Token not found in response.")
                return None
        else:
            print(f"Failed to retrieve token: {response.status_code} - {response.text}")
            return None

    def get_destination_code(self, city_name):
        if not self._token:
            print("No valid token available.")
            return "Not Found"

        headers = {"Authorization": f"Bearer {self._token}"}
        query = {
            "keyword": city_name,
            "max": "2",
            "include": "AIRPORTS",
        }
        response = requests.get(url=IATA_ENDPOINT, headers=headers, params=query)
        if response.status_code == 200:
            try:
                code = response.json()["data"][0]['iataCode']
                return code
            except (IndexError, KeyError) as e:
                print(f"Error extracting IATA code: {e}")
                return "Not Found"
        else:
            print(f"Failed to get destination code: {response.status_code} - {response.text}")
            return "Not Found"

    def check_flights(self, origin_city_code, destination_city_code, from_time, to_time, is_direct=True):
        if not self._token:
            print("No valid token available.")
            return None

        headers = {"Authorization": f"Bearer {self._token}"}
        query = {
            "originLocationCode": origin_city_code,
            "destinationLocationCode": destination_city_code,
            "departureDate": from_time.strftime("%Y-%m-%d"),
            "returnDate": to_time.strftime("%Y-%m-%d"),
            "adults": 1,
            "nonStop": "true" if is_direct else "false",
            "currencyCode": "USD",
            "max": "10",
        }

        response = requests.get(url=FLIGHT_ENDPOINT, headers=headers, params=query)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to check flights: {response.status_code} - {response.text}")
            return None

    def find_cheapest_dates_in_month(self, origin, destination, year, month, num_days=5):
        first_day = datetime(year, month, 1)
        last_day = (first_day.replace(day=28) + timedelta(days=4)).replace(day=1) - timedelta(days=1)
        date_range = [first_day + timedelta(days=i) for i in range((last_day - first_day).days + 1)]
        date_range = date_range[:num_days]

        cheapest_price = float('inf')
        cheapest_date = None

        for date in date_range:
            date_str = date.strftime('%Y-%m-%d')
            price = self.get_cheapest_flight_price(origin, destination, date_str)
            if price is not None and price < cheapest_price:
                cheapest_price = price
                cheapest_date = date_str

        return cheapest_date, cheapest_price

    def get_cheapest_flight_price(self, origin, destination, date):
        try:
            headers = {'Authorization': f'Bearer {self._token}'}
            params = {
                'originLocationCode': origin,
                'destinationLocationCode': destination,
                'departureDate': date,
                'returnDate': (datetime.strptime(date, '%Y-%m-%d') + timedelta(days=7)).strftime('%Y-%m-%d'),
                'adults': 1,
                'currencyCode': 'USD',
                'max': 1
            }
            response = requests.get(FLIGHT_ENDPOINT, headers=headers, params=params)
            data = response.json()

            if data['data']:
                return float(data['data'][0]['price']['grandTotal'])
            return None

        except Exception as e:
            print(f"Error fetching flight price: {e}")
            return None
