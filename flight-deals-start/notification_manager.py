import os
from twilio.rest import Client
import smtplib


class NotificationManager:

    def __init__(self):
        self.smtp_address = os.environ.get("EMAIL_PROVIDER_SMTP_ADDRESS")
        self.smtp_port = int(os.environ.get("EMAIL_PROVIDER_SMTP_PORT", 587))  # Default to 587 if not set
        self.email = os.environ.get("MY_EMAIL")
        self.email_password = os.environ.get("MY_EMAIL_PASSWORD")
        self.twilio_virtual_number = os.environ.get("TWILIO_VIRTUAL_NUMBER")
        self.twilio_verified_number = os.environ.get("TWILIO_VERIFIED_NUMBER")
        self.whatsapp_number = os.environ.get("TWILIO_WHATSAPP_NUMBER")
        self.client = Client(os.environ.get('TWILIO_SID'), os.environ.get("TWILIO_AUTH_TOKEN"))

    def _connect_smtp(self):
        if self.smtp_port == 465:
            return smtplib.SMTP_SSL(self.smtp_address, self.smtp_port)
        else:
            connection = smtplib.SMTP(self.smtp_address, self.smtp_port)
            connection.starttls()
            return connection

    def send_sms(self, message_body):
        message = self.client.messages.create(
            from_=self.twilio_virtual_number,
            body=message_body,
            to=self.twilio_verified_number
        )
        print(f"SMS sent with SID: {message.sid}")

    def send_whatsapp(self, message_body):
        message = self.client.messages.create(
            body=message_body,
            from_=f"whatsapp:{self.whatsapp_number}",
            to=f"whatsapp:{self.twilio_verified_number}"
        )
        print(f"WhatsApp message sent with SID: {message.sid}")

    def send_emails(self, email_list, email_body):
        connection = None
        try:
            connection = self._connect_smtp()
            connection.login(self.email, self.email_password)
            for email in email_list:
                msg = f"Subject: New Low Price Flight!\n\n{email_body}"
                connection.sendmail(from_addr=self.email, to_addrs=email, msg=msg)
                print(f"Email sent to {email}")

        except Exception as e:
            print(f"Failed to send email: {e}")

        finally:
            if connection:
                try:
                    connection.quit()
                except Exception as e:
                    print(f"Failed to close the connection: {e}")

# import os
# from twilio.rest import Client
# import smtplib
#
#
# class NotificationManager:
#
#     def __init__(self):
#         self.smtp_address = os.environ.get("EMAIL_PROVIDER_SMTP_ADDRESS")
#         self.email = os.environ.get("MY_EMAIL")
#         self.email_password = os.environ.get("MY_EMAIL_PASSWORD")
#         self.twilio_virtual_number = os.environ.get("TWILIO_VIRTUAL_NUMBER")
#         self.twilio_verified_number = os.environ.get("TWILIO_VERIFIED_NUMBER")
#         self.whatsapp_number = os.environ.get("TWILIO_WHATSAPP_NUMBER")
#         self.client = Client(os.environ.get('TWILIO_SID'), os.environ.get("TWILIO_AUTH_TOKEN"))
#         self.connection = smtplib.SMTP(os.environ.get("EMAIL_PROVIDER_SMTP_ADDRESS"))
#
#     def send_sms(self, message_body):
#         """
#         Sends an SMS message through the Twilio API.
#         This function takes a message body as input and uses the Twilio API to send an SMS from
#         a predefined virtual number (provided by Twilio) to your own "verified" number.
#         It logs the unique SID (Session ID) of the message, which can be used to
#         verify that the message was sent successfully.
#         Parameters:
#         message_body (str): The text content of the SMS message to be sent.
#         Returns:
#         None
#         Notes:
#         - Ensure that `TWILIO_VIRTUAL_NUMBER` and `TWILIO_VERIFIED_NUMBER` are correctly set up in
#         your environment (.env file) and correspond with numbers registered and verified in your
#         Twilio account.
#         - The Twilio client (`self.client`) should be initialized and authenticated with your
#         Twilio account credentials prior to using this function when the Notification Manager gets
#         initialized.
#         """
#         message = self.client.messages.create(
#             from_=os.environ["TWILIO_VIRTUAL_NUMBER"],
#             body=message_body,
#             to=os.environ["TWILIO_VERIFIED_NUMBER"]
#         )
#         # Prints if successfully sent.
#         print(message.sid)
#
#     # Is SMS not working for you or prefer whatsapp? Connect to the WhatsApp Sandbox!
#     # https://console.twilio.com/us1/develop/sms/try-it-out/whatsapp-learn
#     def send_whatsapp(self, message_body):
#         message = self.client.messages.create(
#             body=message_body,
#             from_=f"whatsapp:{self.whatsapp_number}",  # Replace with your Twilio WhatsApp-enabled number
#             to=f"whatsapp:{self.twilio_verified_number}"  # Replace with a valid recipients WhatsApp-enabled number
#         )
#         print(message.sid)
#
#     def send_emails(self, email_list, email_body):
#         with self.connection:
#             self.connection.starttls()
#             self.connection.login(self.email, self.email_password)
#             for email in email_list:
#                 self.connection.sendmail(
#                     from_addr=self.email,
#                     to_addrs=email,
#                     msg=f"Subject:New Low Price Flight!\n\n{email_body}".encode('utf-8')
#                 )
