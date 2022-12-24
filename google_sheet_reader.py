import gspread
import pandas as pd
from google.oauth2.credentials import Credentials


def get_sheet():
    # Replace with your own Google Sheet ID and range
    spreadsheet_id = '18VRUvWIsn1t1KwDlEroACaPeNjPvc4jBbVkXYDzg1ro'
    sheet_range = 'Sheet1!A1:Z1000'
    # Use the credentials object to authenticate with Google Sheets API
    client = gspread.service_account(filename='/Users/thomaswieringa/Documents/Persoonlijke projecten/langspeelplatendieikwil/venv/lib/python3.9/site-packages/gspread/service_account.json')
    # Open the Google Sheet
    sheet = client.open_by_key(spreadsheet_id).sheet1
    # Read the data from the Google Sheet into a Pandas dataframe
    df = pd.DataFrame(sheet.get_all_values())
    # Set the column names of the dataframe
    df.columns = df.iloc[0]
    # Remove the first row, which contains the column names
    df = df[1:]
    # Print the dataframe to verify that it was correctly read
    return df