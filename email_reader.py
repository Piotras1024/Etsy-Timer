from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle
import os.path
import re
import base64
from dateutil import parser
import random

class EmailReader:
    # def __init__(self, credentials_file='credentials.json', token_file='token.pickle', scopes=['https://www.googleapis.com/auth/gmail.readonly']):
    def __init__(self, credentials_file='credentials.json', token_file='token.pickle', scopes=None):
        if scopes is None:
            scopes = ['https://www.googleapis.com/auth/gmail.readonly']
        self.credentials_file = credentials_file
        self.token_file = token_file
        self.scopes = scopes
        self.service = self.get_gmail_service()

    def get_gmail_service(self):
        creds = None
        # Token file stores the user's access and refresh tokens.
        if os.path.exists(self.token_file):
            with open(self.token_file, 'rb') as token:
                creds = pickle.load(token)
        # If there are no valid credentials, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_file, self.scopes)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(self.token_file, 'wb') as token:
                pickle.dump(creds, token)

        service = build('gmail', 'v1', credentials=creds)
        return service

    def read_emails(self, sender):
        try:
            # Wyszukuje wiadomości od określonego nadawcy
            response = self.service.users().messages().list(userId='me', q=f'from:{sender}').execute()
            messages = response.get('messages', [])

            emails_info = []
            for message in messages:
                msg = self.service.users().messages().get(userId='me', id=message['id'], format='full').execute()

                # Dekodowanie treści e-maila
                message_parts = msg['payload'].get('parts', None)
                message_raw = message_parts[0]['body']['data'] if message_parts else None
                if message_raw:
                    message_content = base64.urlsafe_b64decode(message_raw.encode('ASCII')).decode('utf-8')
                else:
                    continue  # Przechodzi do następnej wiadomości, jeśli nie można zdekodować treści

                # Wyszukiwanie daty
                date_header = msg['payload']['headers']
                date_list = [d['value'] for d in date_header if d['name'] == 'Date']
                date_str = date_list[0] if date_list else ''
                date = parser.parse(date_str)

                # Wyszukiwanie informacji o zamówieniu
                subtotal_match = re.search(r'Subtotal:\s*€(\d+\.\d+)', message_content)
                order_total_match = re.search(r'Order total:\s*€(\d+\.\d+)', message_content)
                pattern = r'<https://www\.etsy\.com/transaction/.*?>(.*?)<https://www\.etsy\.com/transaction'
                collection_name_match = re.search(pattern, message_content, re.DOTALL)

                order_total = order_total_match.group(1) if order_total_match else 'Brak informacji'
                subtotal = subtotal_match.group(1) if subtotal_match else order_total
                collection_name = collection_name_match.group(1) if collection_name_match else 'Brak informacji'
                # collection_name = collection_name_match.group(
                #     0).strip() if collection_name_match else 'Brak informacji'

                # Dodawanie przetworzonych informacji do listy
                emails_info.append({
                    'date': date.strftime('%Y/%m/%d %H:%M'),
                    'hour': date.strftime('%H:%M'),
                    'subtotal': subtotal,
                    'collection_name': collection_name[2:]
                })

            return emails_info

        except Exception as error:
            print(f"Wystąpił błąd: {error}")
            return None

    def read_whole_random_email(self, sender):
        try:
            # Wyszukuje wiadomości od określonego nadawcy
            response = self.service.users().messages().list(userId='me', q=f'from:{sender}').execute()
            messages = response.get('messages', [])

            if not messages:
                return "Nie znaleziono wiadomości od tego nadawcy."

            # Wybierz losową wiadomość
            random_message = random.choice(messages)

            # Pobierz pełną treść e-maila
            msg = self.service.users().messages().get(userId='me', id=random_message['id'], format='full').execute()

            # Dekodowanie treści e-maila
            message_parts = msg['payload'].get('parts', None)
            message_raw = message_parts[0]['body']['data'] if message_parts else None
            if message_raw:
                message_content = base64.urlsafe_b64decode(message_raw.encode('ASCII')).decode('utf-8')
                return message_content
            else:
                return "Nie można zdekodować treści wiadomości."

        except Exception as error:
            return f"Wystąpił błąd: {error}"


email_reader = EmailReader()
emails_from_sender = email_reader.read_emails('forestica.creations@gmail.com')
# Przykładowe wyświetlenie zawartości e-maili
for email in emails_from_sender:
    print(f"Data: {email['date']}, Hour: {email['hour']}, Subtotal: {email['subtotal']}, Collection Name: {email['collection_name']}")

