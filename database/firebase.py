import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import firestore
import os
from dotenv import load_dotenv
import pandas as pd

# getting environmental variables to access db
load_dotenv()

# # Fetch the service account key JSON file contents
service_key_path = os.getenv('service_key')

cred = credentials.Certificate(service_key_path)
firebase_admin.initialize_app(cred)

db = firestore.client()
db_ref = db.collection(u'season')

# Reading the csv file of season stats data frame obtained in database_build
df = pd.read_csv('./season_stats_dataframe.csv', index_col=False)
# Renaming index to ncaa_id
df.rename(columns={'Unnamed: 0': 'ncaa_id'}, inplace=True)

# Turning df to dictionary for uploading to firestore
df_dict = df.to_dict(orient='records')

# Add season stats to firebase with the ncaa_id key as the document id
list(map(lambda team: db_ref.add(team, str(team['ncaa_id'])), df_dict))

