import os

from email_reader import emails_from_sender
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

SPREADSHEET_ID = '1Xbeji-pS8YXKw5U3wNmL19H93FSxoEVcDHIXYJGtbH4'


def main():
    credentials = None
    if os.path.exists("token.json"):
        credentials = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            credentials = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(credentials.to_json())

    try:
        service = build("sheets", "v4", credentials=credentials)
        sheets = service.spreadsheets()

        for index, row in enumerate(emails_from_sender):
            hour = row['hour']
            data = row['date']
            subtotal = row['subtotal']
            collection_name = row['collection_name']

            sheets.values().update(spreadsheetId=SPREADSHEET_ID, range=f"Sheet1!A{index+2}",
                                   valueInputOption="USER_ENTERED", body={"values": [[f"{data}"]]}).execute()
            sheets.values().update(spreadsheetId=SPREADSHEET_ID, range=f"Sheet1!B{index+2}",
                                   valueInputOption="USER_ENTERED", body={"values": [[f"{hour}"]]}).execute()
            sheets.values().update(spreadsheetId=SPREADSHEET_ID, range=f"Sheet1!C{index+2}",
                                   valueInputOption="USER_ENTERED", body={"values": [[f"{subtotal}"]]}).execute()
            sheets.values().update(spreadsheetId=SPREADSHEET_ID, range=f"Sheet1!D{index+2}",
                                   valueInputOption="USER_ENTERED", body={"values": [[f"{collection_name}"]]}).execute()


        # result = sheets.values().get(spreadsheetId=SPREADSHEET_ID, range="Sheet1!A1:C6").execute()

    except HttpError as error:
        print(error)


if __name__ == "__main__":
    main()
