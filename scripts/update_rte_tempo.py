import datetime

"""
Script for RTE API data. 

This script is user dependant ! Please change client ID and client scret code before using it. 
working directory are also case dependant. 

date: 20/06/2019
"""

client_id = '7699170f-9898-40d0-b78a-354bae1f36e6'
client_secret = '969de489-1dca-4158-8ad4-9e1ab405cfeb'

start_date = datetime.datetime.today() - datetime.timedelta(days=2)
end_date   = datetime.datetime.today() + datetime.timedelta(days=1)

# Demande d’access token au serveur d’autorisation
token_type, access_token = get_token(client_id=client_id, client_secret=client_secret)

# Requetes aux service tempo et prod + traitement
r_tempo = get_tempo(start_date, end_date, token_type, access_token)

# Mise sous pandas DataFrame des données json
df_tempo = json_to_pd_tempo(r_tempo)

#%% Sauvegarde des données
import os
import pandas as pd

wd = os.path.dirname(os.path.abspath(__file__))
os.chdir(wd)
os.chdir('../data/')

# sauvegarde des données tempo :
WD = os.getcwd()
file_name_tempo = os.path.join(WD, 'RTE_tempo_data')

if os.path.isfile(file_name_tempo+'.csv'):
    from shutil import copyfile
    copyfile(file_name_tempo+'.csv', file_name_tempo+'_old'+'.csv')

    # reading existing file
    with open(file_name_tempo+'.csv', 'r+', encoding='utf-8') as f:
        df_old = pd.read_csv(f, index_col='start_date', parse_dates=True,
                             usecols=['start_date', 'end_date', 'updated_date', 'value'])
        df_old['start_date'] = df_old.index

    f.close()

    # overwrite old file with new df
    with open(file_name_tempo+'.csv', 'w', encoding='utf-8') as f:
        df = pd.concat([df_old, df_tempo], sort=True)
        df2 = df.loc[~df.index.duplicated(keep='first')]
        df3 = df2.sort_values(by=['start_date'])
        df3.to_csv(f, encoding='utf-8')

else:
    # create a new file
    with open(file_name_tempo+'.csv', 'x', encoding='utf-8') as f:
        df_tempo.to_csv(f, encoding='utf-8')

