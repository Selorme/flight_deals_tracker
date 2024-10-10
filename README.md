# Flight Deal Finder

This project is a flight deal finder that automates the process of searching for the cheapest flights from a specified origin city to multiple destinations. It uses a Google Sheet for managing destination data, updates IATA codes, and sends notifications when flight prices drop below a specified threshold. Notifications are sent via WhatsApp, and emails are sent to all subscribed users.

## Features

1. **Flight Search Automation**: Automatically search for the cheapest direct or indirect flights for multiple destinations.
2. **IATA Code Updates**: Updates missing IATA codes for destination cities in a Google Sheet.
3. **Price Alerts**: Sends low-price alerts via WhatsApp and emails when a cheaper flight is found.
4. **Customizable Search Period**: Users can set the month and number of days to search for flights.
5. **Customer Email List Management**: Retrieves and uses customer emails from a Google Sheet for notifications.

## Requirements

- **Python 3.x**
- **Google Sheets API** to access and update your sheet.
- **Twilio** or another service to send WhatsApp notifications.
- **SMTP Server** to send email notifications.
- **Flight Search API** for retrieving flight details.

## How It Works

1. **Flight Search Setup**:  
   Initializes the necessary services such as `DataManager`, `FlightSearch`, and `NotificationManager`.

2. **Update IATA Codes**:  
   Checks the destination data for missing IATA codes and updates them using the `FlightSearch` service.

3. **Flight Search and Price Comparison**:  
   For each destination, the program finds the cheapest flight in a specified month and compares the price with the stored "lowest price" in the Google Sheet.

4. **Stopover Flights (if no direct flights)**:  
   If no direct flight is found, the script will search for indirect flights as an alternative.

5. **Send Notifications**:  
   If a cheaper price is found, the program sends a notification via WhatsApp and email to all subscribers.

## Setup Instructions

### 1. Install Dependencies
You will need to install the required libraries to run the script. You can do so by running:
```bash
pip install requests pandas twilio
```

### 2. Google Sheets API Setup
- Enable the Google Sheets API and download the `credentials.json` file.
- Place the credentials file in your project directory.
- Use the Google Sheets API to manage your flight data and customer emails.

### 3. Flight Search API Setup
- Sign up for a flight search API (like Tequila by Kiwi.com).
- Use the API key to enable the script to search for flights.

### 4. Notification Setup
- For **WhatsApp Notifications**:  
  Set up a Twilio account and configure your WhatsApp sender.
- For **Email Notifications**:  
  Set up an SMTP server and configure the sender email.

### 5. Configure the Script
- Set your origin city IATA code (e.g., `"IST"` for Istanbul).
- Define the month and number of days for which you want to search for flights.

```python
ORIGIN_CITY_IATA = "IST"
month = 12  # December
year = 2024
num_days = 5  # Number of days to check
```

### 6. Run the Script
Simply run the script to start searching for flights and sending notifications:
```bash
python main.py
```

## Notifications

- **WhatsApp**: Sends a low-price alert message via WhatsApp.
- **Email**: Sends an email to all subscribers with the flight details.

## Example Output

```text
Getting flights for London...
London: Cheapest price is $300 on 2024-12-15
Check your email. Lower price flight found to London!
```

## Future Improvements

- Add SMS notifications via Twilio.
- Implement a graphical interface for easier setup and usage.
- Integrate stopover flight handling for more complex flight itineraries.

## License

This project is licensed under the MIT License.