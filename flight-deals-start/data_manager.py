import requests
import os
from dotenv import load_dotenv

load_dotenv()


class DataManager:

    def __init__(self):
        self.bearer_token = os.environ["SHEETY_BEARER_AUTH_TOKEN"]
        self.headers = {
            "Authorization": f"Bearer {self.bearer_token}",
            "Content-Type": "application/json"
        }
        self.prices_endpoint = os.environ["SHEETY_PRICES_ENDPOINT"]
        self.users_endpoint = os.environ["SHEETY_USERS_ENDPOINT"]
        self.destination_data = {}
        self.customer_data = {}

    def get_destination_data(self):
        try:
            response = requests.get(url=self.prices_endpoint, headers=self.headers)
            response.raise_for_status()
            data = response.json()
            # print("Response JSON:", data)
            self.destination_data = data.get("prices", [])
            return self.destination_data
        except requests.exceptions.RequestException as e:
            print(f"Error getting destination data: {e}")
            return []

    def update_destination_codes(self):
        try:
            for city in self.destination_data:
                new_data = {
                    "price": {
                        "iataCode": city["iataCode"]
                    }
                }
                response = requests.put(
                    url=f"{self.prices_endpoint}/{city['id']}",
                    json=new_data,
                    headers=self.headers  # Ensure headers are included in the PUT request
                )
                response.raise_for_status()
                print(response.text)
        except requests.exceptions.RequestException as e:
            print(f"Error updating destination codes: {e}")

    def get_customer_emails(self):
        response = requests.get(url=self.users_endpoint, headers=self.headers)
        data = response.json()
        self.customer_data = data["users"]
        return self.customer_data


# Example usage
if __name__ == "__main__":
    data_manager = DataManager()
    sheet_data = data_manager.get_destination_data()
    print(sheet_data)
    # Assuming you have updated the IATA codes in sheet_data
    data_manager.update_destination_codes()
