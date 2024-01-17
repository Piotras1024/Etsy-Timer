import os
from email_reader import emails_from_sender
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SPREADSHEET_ID = '1Xbeji-pS8YXKw5U3wNmL19H93FSxoEVcDHIXYJGtbH4'


def get_credentials():
    if os.path.exists("token.json"):
        credentials = Credentials.from_authorized_user_file("token.json", SCOPES)
    else:
        flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
        credentials = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(credentials.to_json())
    if credentials.expired and credentials.refresh_token:
        credentials.refresh(Request())
    return credentials


def get_sheets(credentials):
    try:
        service = build("sheets", "v4", credentials=credentials)
        return service.spreadsheets()
    except HttpError as error:
        print(error)
        return None


def update_sheet_value(sheets, range, value):
    try:
        sheets.values().update(
            spreadsheetId=SPREADSHEET_ID,
            range=range,
            valueInputOption="USER_ENTERED",
            body={"values": [[value]]}
        ).execute()
    except HttpError as error:
        print(error)


def main():
    credentials = get_credentials()
    sheets = get_sheets(credentials)

    if sheets is not None:
        for index, row in enumerate(emails_from_sender):
            update_sheet_value(sheets, f"Sheet1!A{index+2}", row['date'])
            update_sheet_value(sheets, f"Sheet1!B{index+2}", row['hour'])
            update_sheet_value(sheets, f"Sheet1!C{index+2}", row['subtotal'])
            update_sheet_value(sheets, f"Sheet1!D{index+2}", row['collection_name'])


if __name__ == "__main__":
    main()
