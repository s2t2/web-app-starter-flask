
# adapted from: https://www.twilio.com/blog/2017/02/an-easy-way-to-read-and-write-to-a-google-spreadsheet-in-python.html

from dotenv import load_dotenv
import os

import gspread
from gspread.exceptions import SpreadsheetNotFound
from oauth2client.service_account import ServiceAccountCredentials

load_dotenv()

DOCUMENT_KEY = os.environ.get("GOOGLE_SHEET_ID", "OOPS Please get the spreadsheet identifier from its URL")
SHEET_NAME = "Products"

#
# AUTHORIZATION
# ... https://developers.google.com/sheets/api/guides/authorizing
# ... https://gspread.readthedocs.io/en/latest/oauth2.html
#

CREDENTIALS_FILEPATH = os.path.join(os.path.dirname(__file__), "..", "auth", "spreadsheet_credentials.json")

AUTH_SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets", #> Allows read/write access to the user's sheets and their properties.
    "https://www.googleapis.com/auth/drive.file" #> Per-file access to files created or opened by the app.
]


if __name__ == "__main__":
    pass

    credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILEPATH, AUTH_SCOPE)

    #
    # READ SHEET VALUES
    #

    client = gspread.authorize(credentials) #> <class 'gspread.client.Client'>

    doc = client.open_by_key(DOCUMENT_KEY) #> <class 'gspread.models.Spreadsheet'>

    print("-----------------")
    print("SPREADSHEET:", doc.title)
    print("-----------------")

    sheet = doc.worksheet(SHEET_NAME) #> <class 'gspread.models.Worksheet'>

    rows = sheet.get_all_records() #> <class 'list'>

    for row in rows:
        print(row) #> <class 'dict'>

    #
    # WRITE VALUES TO SHEET
    #

    next_id = len(rows) + 1 # number of records, plus one. TODO: max of current ids, plus one
    next_row_number = len(rows) + 2 # number of records, plus a header row, plus one

    product = {
        "id": next_id,
        "name": f"Product {next_id}",
        "department": "snacks",
        "price": 4.99,
        "availability_date": "2019-01-01"
    }

    next_row = list(product.values())

    response = sheet.insert_row(next_row, next_row_number)

    print("ADDING A RECORD...")
    # print(type(response)) #> dict
    # print(response) #> {'spreadsheetId': 'abc123', 'updatedRange': 'Products!A5:C5', 'updatedRows': 1, 'updatedColumns': 3, 'updatedCells': 3}

    print(f"UPDATED RANGE: '{response['updatedRange']}' ({response['updatedCells']} CELLS)")