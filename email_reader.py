from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle
import os.path


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

            emails = []
            if not messages:
                print("Nie znaleziono wiadomości od:", sender)
            else:
                print(f"Znaleziono {len(messages)} wiadomości od {sender}")
                for message in messages:
                    msg = self.service.users().messages().get(userId='me', id=message['id']).execute()
                    emails.append(msg)

            return emails

        except Exception as error:
            print(f"Wystąpił błąd: {error}")
            return None


email_reader = EmailReader()
emails_from_sender = email_reader.read_emails('forestica.creations@gmail.com')
# Przykładowe wyświetlenie zawartości e-maili
for email in emails_from_sender:
    print(email['snippet'])  # 'snippet' zawiera krótki fragment treści e-maila
