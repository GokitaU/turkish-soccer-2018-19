from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

import pandas as pd

'''Google code for importing data from Google Sheets into a DataFrame
below.''' 
# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1EtogzMDJyPulNrLZyqieDFqWPh6lyv1qyGwnxZo8tIo'
SAMPLE_RANGE_NAME = 'super_lig_2018_19'

def main():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
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

    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                range=SAMPLE_RANGE_NAME).execute()
    values = result.get('values', [])

    for i in range(len(values)):
        values[i].pop(1)
     
    cols = values.pop(0)
    df = pd.DataFrame(values,columns=cols)
    df.rename(columns={ df.columns[1]: "new_col_name" })
    del df['R']
    
    '''Easiest way of fixing team values and make them easy to search for
    using Regex and Pandas filtering.'''
    
    df.replace(to_replace='.Galatasaray',value=' GS',inplace=True,regex=True)
    df.replace(to_replace='.Fenerbahce',value=' FB',inplace=True,regex=True)
    df.replace(to_replace='.Besiktas',value=' BJK',inplace=True,regex=True)
    df.replace(to_replace='.Ankaragucu',value=' ANK',inplace=True,regex=True)
    df.replace(to_replace='.Istanbul Basaksehir',value=' IBFK',inplace=True,regex=True)
    df.replace(to_replace='.Kayserispor',value=' KAY',inplace=True,regex=True)
    df.replace(to_replace='.Konyaspor',value=' KON',inplace=True,regex=True)
    df.replace(to_replace='.Kasimpasa',value=' KAS',inplace=True,regex=True)
    df.replace(to_replace='.Alanyaspor',value=' ALN',inplace=True,regex=True)
    df.replace(to_replace='.Sivasspor',value=' SIV',inplace=True,regex=True)
    df.replace(to_replace='.Bursaspor',value=' BUR',inplace=True,regex=True)
    df.replace(to_replace='.Erzurum BB',value=' ERZ',inplace=True,regex=True)
    df.replace(to_replace='.Trabzonspor',value=' TS',inplace=True,regex=True)
    df.replace(to_replace='.Antalyaspor',value=' ANT',inplace=True,regex=True)
    df.replace(to_replace='.Rizespor',value=' RIZE',inplace=True,regex=True)
    df.replace(to_replace='.Akhisarspor',value=' AKH',inplace=True,regex=True)
    df.replace(to_replace='.Goztepe',value=' GOZ',inplace=True,regex=True)
    df.replace(to_replace='.Yeni Malatyaspor',value=' YMS',inplace=True,regex=True)
       
    
    goalkeeper = df[df.Pos1.str.contains('G.')]
    defender = df[df.Pos1.str.contains('D\(.') | 
            df.Pos2.str.contains('D\(.')]
    midfielder = df[df.Pos1.str.contains('.?M\(?.')| 
            df.Pos2.str.contains('.?M\(.')]
        
    forward= df[df.Pos1.str.contains('F.') |
            df.Pos2.str.contains('F.')]
    
    defender = defender.sort_values(by=['Drb','Crosses','KeyP','ThrB'],
                               ascending=False)
    
    '''Some example searches below.'''
    
    young_midfielders = midfielder[pd.to_numeric(midfielder['Age'])<=25)]
    print(young_midfielders)
#        
if __name__ == '__main__':
    main()