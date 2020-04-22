from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

import pandas as pd

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# The ID and range of a sample spreadsheet.
SPREADSHEET_ID = '1Qew2IsSQtkQbF78zJ_FQZqAd3psR1rDtj4bXLaGb0z4'
RANGE_NAME = 'StatePrevalenceProgression!A3:T12'


def loginWithCredentials():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return build('sheets', 'v4', credentials=creds)


def extractDataFromSheet(Service, SheetID, RangeName): 
    # Call the Sheets API
    sheet = Service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SheetID,
                                range=RangeName).execute()
    values = result.get('values', [])

    if not values:
        print('No data found. Try again.')

    else:
        return values

def main():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    service = loginWithCredentials()

    values = extractDataFromSheet(service, SPREADSHEET_ID, RANGE_NAME)
    
    dates = [str(i[0]) for i in values]
    dates = dates[1:]

    states = values[0]
    states = states[2:]

    # State   Date1   Date2   Date3   Date4   ... 
    # State   Prev    Prev    Prev    Prev   ... 
    # State   Prev    Prev    Prev    Prev   ... 
    # State   Prev    Prev    Prev    Prev   ... 

    data = {
        'States':  states,
        'StateID': ["01", "02", "03", "04", "05", "06", "07", "08", "09", "11", "12", "10", "13", "14", "15", "16", "17", "18"],
        }

    for j in range(len(dates)):
        data[dates[j]] = values[j+1][2:]  ## taking prevalence values into dates
        data[dates[j]] = [float(i) for i in data[dates[j]]] ## convert strings into floats

    df = pd.DataFrame(data)

    ## make all KL, Selangor & Putrajaya the same prevalence 
    for k in range(len(df.columns)):
        if k >= 2:
            df.iat[0,k] = df.iat[16,k]
            df.iat[2,k] = df.iat[16,k]
            df.iat[14,k] = df.iat[16,k]

    print(df)

if __name__ == '__main__':
    main()