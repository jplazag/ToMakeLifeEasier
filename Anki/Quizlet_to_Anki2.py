import pygsheets
import pandas as pd
import sys
import os

deutsch_m = []
deutsch_f = []
deutsch_n = []
deutsch_andere = []

spanisch_m = []
spanisch_f = []
spanisch_n = []
spanisch_andere = []


#authorization
gc = pygsheets.authorize(service_file='ToIgnore/client_secret.json')

# Create empty dataframe
df = pd.DataFrame()

#open the google spreadsheet (where 'PY to Gsheet Test' is the name of my sheet)
sh = gc.open('Anki')

#select the sheet 
wks = sh[1]

#take the name of the sheet
title = wks.title

#Create a new directory with the name of the sheet in case it doesn't exist
if not os.path.exists('Private/' + title):
    os.makedirs('Private/' + title)
    print("The directory " + title + " was created!")


#transform the data from the sheet to a dataframe
df = wks.get_as_df()

for frontTerm, backTerm in df.itertuples(index=False):
    
    #clasify the terms in the sheet depending on the german articles
    if(frontTerm[0:3] == "der"):

        deutsch_m.append(frontTerm)
        spanisch_m.append(backTerm[0:-1])
    
    elif(frontTerm[0:3] == "die"):

        deutsch_f.append(frontTerm)
        spanisch_f.append(backTerm[0:-1])

    elif(frontTerm[0:3] == "das"):

        deutsch_n.append(frontTerm)
        spanisch_n.append(backTerm[0:-1])

    else:
        deutsch_andere.append(frontTerm)
        spanisch_andere.append(backTerm[0:-1])

    #create the dictionaries with the clasified terms
    anki_m = {"Deutsch": deutsch_m, "Spanisch": spanisch_m}

    anki_f = {"Deutsch": deutsch_f, "Spanisch": spanisch_f}

    anki_n = {"Deutsch": deutsch_n, "Spanisch": spanisch_n}

    anki_andere = {"Deutsch": deutsch_andere, "Spanisch": spanisch_andere}

    
    #converts those dictionaries in dataframes to save them in txt files
    df_m = pd.DataFrame(anki_m)

    df_f = pd.DataFrame(anki_f)

    df_n = pd.DataFrame(anki_n)

    df_andere = pd.DataFrame(anki_andere)


    if not df_m.empty:

        df_m.to_csv('Private/' + title + '/' + title + ' - mannlich.txt',index=False, header=False, sep='\t', encoding = 'utf-8')

    if not df_f.empty:

        df_f.to_csv('Private/' + title + '/' + title + ' - weblich.txt',index=False, header=False, sep='\t', encoding = 'utf-8')

    if not df_n.empty:

        df_n.to_csv('Private/' + title + '/' + title + ' - neutrum.txt',index=False, header=False, sep='\t', encoding = 'utf-8')

    if not df_andere.empty:
        
        df_andere.to_csv('Private/' + title + '/' + title + '.txt',index=False, header=False, sep='\t', encoding = 'utf-8')






