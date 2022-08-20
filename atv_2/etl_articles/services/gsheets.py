# general libraries
import pandas as pd
import json

# google libraries
import gspread
from google.oauth2 import service_account
from google.auth.transport.requests import AuthorizedSession
from oauth2client.service_account import ServiceAccountCredentials
from gspread_dataframe import get_as_dataframe, set_with_dataframe

# environment
from dotenv import load_dotenv
from os import environ


load_dotenv()


def connect_gsheets():
    """Connect in Google Sheets"""

    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive",
    ]

    key_path = json.loads(environ['BIGQUERY_KEY'])

    credentials = service_account.Credentials.from_service_account_info(
        key_path)
    credentials = credentials.with_scopes(scope)
    gc = gspread.Client(auth=credentials)
    gc.session = AuthorizedSession(credentials)

    print(f'gc connect_gsheets: {gc}')

    return gc


def read_gsheets(sheet_id, worksheet_number=1):
    """Read a Google Spreadsheet and return your 
    access and a dataframe"""

    # Se autentica
    gc = connect_gsheets()
    wks = wks = gc.open_by_key(sheet_id)                # sheet_id
    worksheet = wks.get_worksheet(worksheet_number)     # test = 1
    data = worksheet.get_all_values()
    headers = data.pop(0)
    dataframe = pd.DataFrame(data, columns=headers)

    return dataframe


def write_in_gsheets(dataframe):
    gc = connect_gsheets()
    sh = gc.open_by_key(environ['GOOGLE_SHEETS_ID'])
    worksheet_title = "articles"
    try:
        worksheet = sh.worksheet(worksheet_title)
    except gspread.WorksheetNotFound:
        worksheet = sh.add_worksheet(
            title=worksheet_title, rows=1000, cols=1000)
    df_read = read_gsheets(environ['GOOGLE_SHEETS_ID'], 0)
    row = df_read.shape[0]
    print(f"row: {row+2}")
    set_with_dataframe(worksheet, dataframe, row=row +
                       2, include_column_header=False)

    return 'write_in_gsheets: ok'
