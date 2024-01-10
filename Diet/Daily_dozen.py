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

from gensim.models import Word2Vec
from gensim.models import KeyedVectors

from fuzzywuzzy import fuzz

import spacy

import numpy as np

# import en_core_web_sm


word2vec_model_path = "Private/GoogleNews-vectors-negative300.bin.gz"
word_vectors = KeyedVectors.load_word2vec_format(word2vec_model_path, binary=True)


def extract_data_from(scopes, spreadsheets_id, sheet):
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

        result = sheets.values().get(spreadsheetId=spreadsheets_id, range=sheet).execute()

        values = result.get("values", [])

        # for row in values:
        return values

    except HttpError as error:
        print(error)
    

def split_in_groups(extracted_data):

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

    return groups


def find_components_in_database(components_df, food_df):

    for _, row in components_df.iterrows():

        if row["Name"] is None:
            continue
        if "//" in row["Name"]:

            component_name = row["Name"].split(" //")[0]
        else:
            component_name = row["Name"]

        
        print(component_name)
        print(type(component_name))

        # Find the most similar word in the database
        similarities = find_most_similar_word_W2V(component_name, food_df)
        # similarities = find_similar_word_FUZZ(component_name, food_df)
        # similarities = find_most_similar_word(given_product, food_database)

        # Set a threshold for similarity
        threshold = 0.7
        # best_match, best_similarity = similarities[0]

        # if best_similarity >= threshold:
        # print(f"The given product '{component_name}' is likely '{best_match}' with a similarity score of {best_similarity:.2f}.")
        # else:
        #     print(f"No match found for '{component_name}'.")

        print(f"The given product {component_name} is likely {similarities[0:4]}")


def find_most_similar_word_W2V(queries, possible_words):
    
    similarities = []

    queries = queries.replace(".", " ").replace(",", " ")
    queries = queries.split(" ")
    
    for words in possible_words:

        if words is None:
            continue

        words = words.replace(".", " ").replace(",", " ")
        words = words.split(" ")
        
        words_similarities = np.zeros((len(queries), len(words)))

        for i, query in enumerate(queries):

            if query.isnumeric():
                continue

            # if len(words.split(" ")) > 1:
            
        
            # words_similarities = [word_vectors.similarity(query, word.lower()) for word in words]
            # words_similarities = sum(words_similarities) / len(words_similarities)
            
            
            for j, word in enumerate(words):
            
                try:
                    words_similarities[i, j] = word_vectors.similarity(query.lower(), word.lower())
                except Exception as e:
                    # print(e)
                    pass
                
        if np.sum(words_similarities) / ( np.count_nonzero(words_similarities > 0)) > 0.5:
            print("=================================")
            print(queries)
            print(words)
            print("_________________________________")
            print(words_similarities)
            similarities.append((words, np.sum(words_similarities) / ( np.count_nonzero(words_similarities > 0)) ) )

                
            # else:
            #     try:
            #         similarities.append((words, word_vectors.similarity(query.lower(), words.lower())))
            #     except Exception as e:
            #         # print(e)
            #         pass
    
    if len(similarities) is None:
        similarities = [('', 0)]
        
    similarities.sort(key=lambda x: x[1], reverse=True)
    
    return similarities

def find_similar_word_FUZZ(query, possible_words):

    # Calculate similarity using fuzz ratio
    similarities = [(word, fuzz.ratio(query, word)) for word in possible_words]

    similarities.sort(key=lambda x: x[1], reverse=True)

    return similarities

if __name__ == "__main__":

    scopes = ["https://www.googleapis.com/auth/spreadsheets"]

    spreadsheets_id = "1rKlBcD49c0YCyWr_JHsK56XgVMJAlG8zFDOlWocOH_o"

    breakfast_values = extract_data_from(scopes, spreadsheets_id, "Breakfast")

    nutrients_values = extract_data_from(scopes, spreadsheets_id, "Nutrients Values")

    # recipes = split_in_groups(breakfast_values)

    breakfast_df = pd.DataFrame(breakfast_values[1:], columns=breakfast_values[0])

    nutrients_df = pd.DataFrame(nutrients_values[1:], columns=nutrients_values[0])

    find_components_in_database(breakfast_df, nutrients_df["ITEM"])


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