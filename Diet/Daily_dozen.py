# import pygsheets
# import os
# import pandas as pd
# import sys

import os

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import pandas as pd


scopes = ["https://www.googleapis.com/auth/spreadsheets"]

spreadsheets_id = "1rKlBcD49c0YCyWr_JHsK56XgVMJAlG8zFDOlWocOH_o"


def extract_data():
    credentials = None
    if os.path.exists("Private/token.json"):
        credentials = Credentials.from_authorized_user_file("Private/token.json", scopes)
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("Private/credentials.json", scopes)
            credentials = flow.run_local_server(port=0)
        with open("Private/token.json", "w") as token:
            token.write(credentials.to_json())
    
    try:
        service = build("sheets", "v4", credentials=credentials)

        sheets = service.spreadsheets()

        result = sheets.values().get(spreadsheetId=spreadsheets_id, range="Breakfast").execute()

        values = result.get("values", [])

        # for row in values:
        return values

    except HttpError as error:
        print(error)
    

def convert_to_df(extracted_data):

    df = pd.DataFrame(extracted_data[1:], columns=extracted_data[0]) 
    void_row_indices = df[df.isnull().all(axis=1)].index
    
    
    # Split the DataFrame into groups based on void rows
    groups = {}
    start_idx = 0

    for void_idx in void_row_indices:
        if start_idx == void_idx:
            start_idx = void_idx + 1
            continue

        # print(df.iloc[start_idx][0])
        group = df.iloc[start_idx + 1:void_idx]

        group_name = str(df.iloc[start_idx][0])

        group_name = group_name.split(" //")[0]
        print(group_name)
        groups[group_name] = group
        start_idx = void_idx + 1

    # If there are rows after the last void row, add them to the last group
    if start_idx < len(df):
        last_group = df.iloc[start_idx + 1:]

        group_name = str(df.iloc[start_idx][0])

        group_name = group_name.split(" //")[0]

        groups[group_name] = last_group

    # Now, 'groups' is a list of DataFrames, where each DataFrame represents a group of rows separated by void rows
    for i, group_df in enumerate(groups):
        print(f"Group {i + 1}:\n{group_df}\n{'-' * 20}")



if __name__ == "__main__":

    googlesheet_values = extract_data()
    convert_to_df(googlesheet_values)

    


""" import pandas as pd

import re

def convert_google_sheet_url(url):
    # Regular expression to match and capture the necessary part of the URL
    pattern = r'https://docs\.google\.com/spreadsheets/d/([a-zA-Z0-9-_]+)(/edit#gid=(\d+)|/edit.*)?'

    # Replace function to construct the new URL for CSV export
    # If gid is present in the URL, it includes it in the export URL, otherwise, it's omitted
    replacement = lambda m: f'https://docs.google.com/spreadsheets/d/{m.group(1)}/export?' + (f'gid={m.group(3)}&' if m.group(3) else '') + 'format=csv'

    # Replace using regex
    new_url = re.sub(pattern, replacement, url)

    return new_url



# Replace with your modified URL
url = 'https://docs.google.com/spreadsheets/d/1mSEJtzy5L0nuIMRlY9rYdC5s899Ptu2gdMJcIalr5pg/edit#gid=1606352415'

new_url = convert_google_sheet_url(url)

print(new_url)
# https://docs.google.com/spreadsheets/d/1mSEJtzy5L0nuIMRlY9rYdC5s899Ptu2gdMJcIalr5pg/export?gid=1606352415&format=csv

df = pd.read_csv(new_url)


print(df.head()) """