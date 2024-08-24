import pandas as pd 
import glob
import os
import json
import psycopg2
from datetime import datetime, timedelta
from dotenv import load_dotenv
load_dotenv()
import sys
import dotenv
sys.path.append(os.getenv("ROOTPATH"))
from capitaliq.cfg import SERVER_TIMEZONE,DBINFO

transcripts_paths = glob.glob('/Users/zhenggong/Documents/GitHub/transcriptPipeline/data/raw/full_transcript/*.parquet')[0:1000]

res = []
for transcript_path in transcripts_paths:
    sample_transcript = pd.read_parquet(transcript_path)
    sample_transcript = sample_transcript.query('transcriptcomponenttypeid == 3')[['transcriptpersonid', 'transcriptpersonname']].drop_duplicates(subset='transcriptpersonid')
    sample_transcript['tid'] = int(transcript_path.replace('.parquet', '').split('/')[-1].split('_')[0])
    res.append(sample_transcript)
sample_transcript = pd.concat(res)
print(len(sample_transcript))
assert False

sample_transcript = pd.merge(sample_transcript, pd.read_csv('/Users/zhenggong/Documents/GitHub/ba_thesis/data/processed/universeAugmented.csv').rename(columns={"transcriptid":"tid"})[['tid', 'calendaryear']],
                             left_on='tid', right_on='tid')
print(sample_transcript)

# get year range of the analysts
year_range = sample_transcript.groupby('transcriptpersonid')['calendaryear'].agg(['min', 'max']).reset_index()
year_range.columns = ['transcriptpersonid', 'min_year', 'max_year']

# catch some specific case
substring_to_check = 'Unknown'
sample_transcript = sample_transcript.query('~transcriptpersonname.str.contains(@substring_to_check)')
sample_transcript.drop_duplicates(subset='transcriptpersonid', inplace=True)
print(len(sample_transcript))

people_details = get_transcriptperson(sample_transcript['transcriptpersonid'].tolist())
people_details = people_details.dropna(subset=['proid', 'companyname'], how='all')
people_details = pd.merge(people_details, year_range, left_on='transcriptpersonid', right_on='transcriptpersonid')
people_details.sort_values('transcriptpersonname')