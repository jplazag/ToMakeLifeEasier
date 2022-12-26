import sys
import pandas as pd



titel = input("Gib mir einen Titel: \n")

print("Giben Sie mir meine Datai: \n")



msg = sys.stdin.readlines()
# print(msg)

# Du brauchest Ctrl + z, um die input zu beenden

def dataigenerator():

    deutsch_m = []
    deutsch_f = []
    deutsch_n = []
    deutsch_andere = []

    spanisch_m = []
    spanisch_f = []
    spanisch_n = []
    spanisch_andere = []

    for item in msg:
        linie = item.split(" ;")

        if(linie[0][0:3] == "der"):

            deutsch_m.append(linie[0])
            spanisch_m.append(linie[1][0:-1])
        
        elif(linie[0][0:3] == "die"):

            deutsch_f.append(linie[0])
            spanisch_f.append(linie[1][0:-1])

        elif(linie[0][0:3] == "das"):

            deutsch_n.append(linie[0])
            spanisch_n.append(linie[1][0:-1])

        else:
            deutsch_andere.append(linie[0])
            spanisch_andere.append(linie[1][0:-1])

    
    anki_m = {"Deutsch": deutsch_m, "Spanisch": spanisch_m}

    anki_f = {"Deutsch": deutsch_f, "Spanisch": spanisch_f}

    anki_n = {"Deutsch": deutsch_n, "Spanisch": spanisch_n}

    anki_andere = {"Deutsch": deutsch_andere, "Spanisch": spanisch_andere}

    

    df_m = pd.DataFrame(anki_m)

    df_f = pd.DataFrame(anki_f)

    df_n = pd.DataFrame(anki_n)

    df_andere = pd.DataFrame(anki_andere)


    if not df_m.empty:

        df_m.to_csv(titel + ' - mannlich.txt',index=False, header=False, sep='\t', encoding = 'utf-8')

    if not df_f.empty:

        df_f.to_csv(titel + ' - weblich.txt',index=False, header=False, sep='\t', encoding = 'utf-8')

    if not df_n.empty:

        df_n.to_csv(titel + ' - neutrum.txt',index=False, header=False, sep='\t', encoding = 'utf-8')

    if not df_andere.empty:
        
        df_andere.to_csv(titel + '.txt',index=False, header=False, sep='\t', encoding = 'utf-8')

dataigenerator()