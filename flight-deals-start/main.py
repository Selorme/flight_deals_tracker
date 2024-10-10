import time
from datetime import datetime, timedelta
from data_manager import DataManager
from flight_search import FlightSearch
from notification_manager import NotificationManager

# ==================== Set up the Flight Search ====================

data_manager = DataManager()
sheet_data = data_manager.get_destination_data()
flight_search = FlightSearch()
notification_manager = NotificationManager()

# Set your origin airport
ORIGIN_CITY_IATA = "IST"

# ==================== Update the Airport Codes in Google Sheet ====================

for row in sheet_data:
    if row["iataCode"] == "":
        row["iataCode"] = flight_search.get_destination_code(row["city"])
        # slowing down requests to avoid rate limit
        time.sleep(2)
print(f"sheet_data:\n {sheet_data}")

data_manager.destination_data = sheet_data
data_manager.update_destination_codes()

# ==================== Retrieve your customer emails ====================

customer_data = data_manager.get_customer_emails()
# Verify the name of your email column in your sheet. Yours may be different from mine
customer_email_list = [row["whatIsYourEmail?"] for row in customer_data]
# print(f"Your email list includes {customer_email_list}")

# ==================== Search for Direct Flights ====================
month = 12  # December
year = 2024
num_days = 5  # Number of days to check

for destination in sheet_data:
    print(f"Getting flights for {destination['city']}...")
    cheapest_date, cheapest_price = flight_search.find_cheapest_dates_in_month(
        ORIGIN_CITY_IATA,
        destination["iataCode"],
        year,
        month,
        num_days=num_days
    )
    if cheapest_date:
        print(f"{destination['city']}: Cheapest price is ${cheapest_price} on {cheapest_date}")
    else:
        print(f"No flights found for {destination['city']}.")

    # Slowing down requests to avoid rate limit
    time.sleep(2)

    # ==================== Search for indirect flight if N/A ====================

    if cheapest_price == "N/A":
        print(f"No direct flight to {destination['city']}. Looking for indirect flights...")
        stopover_flights = flight_search.check_flights(
            ORIGIN_CITY_IATA,
            destination["iataCode"],
            from_time=datetime.strptime(cheapest_date, '%Y-%m-%d'),
            to_time=(datetime.strptime(cheapest_date, '%Y-%m-%d') + timedelta(days=7)),
            is_direct=False
        )
        # Handle stopover flights
        # ... (similar logic to handle and process stopover flights)

    # ==================== Send Notifications and Emails  ====================

    # Assuming `cheapest_price` is a float value now
    if cheapest_price != "N/A" and cheapest_price < destination["lowestPrice"]:
        message = f"Low price alert! Only USD {cheapest_price} to fly direct " \
                  f"from {ORIGIN_CITY_IATA} to {destination['city']}, " \
                  f"on {cheapest_date}."

        print(f"Check your email. Lower price flight found to {destination['city']}!")

        # notification_manager.send_sms(message_body=message)
        # SMS not working? Try WhatsApp instead.
        notification_manager.send_whatsapp(message_body=message)

        # Send emails to everyone on the list
        notification_manager.send_emails(email_list=customer_email_list, email_body=message)
