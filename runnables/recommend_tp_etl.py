import pandas as pd 
import sys
## ---------- Define Root Path ---------- ## 
ROOTPATH = '/Users/zhenggong/Documents/Github/IBES_selected/' # for importing and reference management 
sys.path.append(ROOTPATH)
from capitaliq.databaseManager import get_company_country

# notes 
# ANNDATS, ANNTIMS: Date and Time when the estimate/ recommendation was released by an analyst
# AMASKCD: the id of analysts, it remains the same across firms when they switch jobs
# ACTDATS, ACTTIMS: Date and Time when the estimate/ recommendation was entered into the database

# param
# cutoff timing 
cutoff = "'2008-01-01'"
ibes_onlyUS = True # by USFIRM == 1
ciqUS = True
# try to match it to CIQ data
cusip = pd.read_parquet('data/ref/isinmap.parquet')[['CusipSedol', 'companyid']].drop_duplicates() # this one can be recalculated from isin-s # this is a legacy file
# print(cusip)

# recommendataions (buy or sell or HOLD)
if True: 
    print('recommend\n')
    # Focus on IRECCD (which is reconciled at IBES level) 
    # etext and ereccd are explicit recommendation (can be less comparable)
    recommend = pd.read_csv('/Users/zhenggong/Documents/GitHub/IBES_selected/IBES_csv/nahghdromygr63ao.csv', index_col=[0])
    recommend['ANNTIMS'] = pd.to_datetime(recommend['ANNTIMS'], format="mixed").dt.time
    recommend['ACTTIMS'] = pd.to_datetime(recommend['ACTTIMS'], format="mixed").dt.time
    _len_recommend = len(recommend)
    # time cutoff
    recommend = recommend.query(f"ANNDATS > {cutoff}").reset_index(drop=True)
    _len_recommend_2 = len(recommend)
    print(f'data shrinking by dropping time cutoff data is {1 - _len_recommend_2/_len_recommend}')

    if ibes_onlyUS:
        recommend = recommend.query("USFIRM == 1.0").reset_index(drop=True) # US firm
        recommend = recommend.drop(columns=['USFIRM'])
        _len_recommend_3 = len(recommend)
        print(f'data shrinking by time cutoff data and US data is {1 - _len_recommend_3/_len_recommend}')

    recommend = pd.merge(recommend, cusip, left_on='CUSIP', right_on='CusipSedol', how='inner')
    _len_recommend_4 = len(recommend)
    print(f'data shrinking by time cutoff data and US data and CUSIP to CIQcompanyid matching is {1 - _len_recommend_4/_len_recommend}')

    if ciqUS:
        country_ref = get_company_country(recommend['companyid'].unique()).drop(columns=['companytypeid'])
        recommend = pd.merge(recommend, country_ref, left_on=['companyid'], right_on=['companyid'], how ='inner')
        recommend = recommend.query('countryid == 213 and incorporationcountryid == 213')
        recommend = recommend.drop(columns=['countryid', 'incorporationcountryid', 'CusipSedol', 'simpleindustryid']).reset_index(drop=True)
        _len_recommend_5 = len(recommend)
        print(f'data shrinking by ciqUS and everything above is {1 - _len_recommend_5/_len_recommend}')     

    # analysis
    num_distinct_analysis = len(recommend['AMASKCD'].unique())
    num_distinct_companies = len(recommend['CUSIP'].unique())
    num_of_records = len(recommend)

    print('some selective statistics:')
    print('-----------------------')
    print('number of records: ' + str(num_of_records))
    print('the number of distinct analysts: ' + str(num_distinct_analysis))
    print('the number of distinct companies: ' + str(num_distinct_companies))

    recommend.to_parquet('IBES_clean_parquet/recommendation.parquet')
    recommend.to_csv('IBES_clean_csv/recommendation.csv')

    print('====================\n')

# target pricing
if True: 
    print('pt\n')
    # Focus on IRECCD (which is reconciled at IBES level) 
    # etext and ereccd are explicit recommendation (can be less comparable)
    pt = pd.read_csv('/Users/zhenggong/Documents/GitHub/IBES_selected/IBES_csv/mvu1wv7ytomyirk4.csv', index_col=[0])
    pt['ANNTIMS'] = pd.to_datetime(pt['ANNTIMS'], format="mixed").dt.time
    pt['ACTTIMS'] = pd.to_datetime(pt['ACTTIMS'], format="mixed").dt.time
    _len_pt = len(pt)
    # time cutoff
    pt = pt.query(f"ANNDATS > {cutoff}").reset_index(drop=True)
    _len_pt_2 = len(pt)
    print(f'data shrinking by time cutoff data is {1 - _len_pt_2/_len_pt}')

    if ibes_onlyUS:
        pt = pt.query("USFIRM == 1.0 and ESTCUR == 'USD' and CURR == 'USD'").reset_index(drop=True) # US firm
        pt = pt.drop(columns=['CURR', 'ESTCUR', 'USFIRM'])
        _len_pt_3 = len(pt)
        print(f'data shrinking by dropping time cutoff data and US data is {1 - _len_pt_3/_len_pt}')

    pt = pd.merge(pt, cusip, left_on='CUSIP', right_on='CusipSedol', how='inner')
    _len_pt_4 = len(pt)
    print(f'data shrinking by time cutoff data and US data and CUSIP to CIQcompanyid matching is {1 - _len_pt_4/_len_pt}')

    if ciqUS:
        country_ref = get_company_country(pt['companyid'].unique()).drop(columns=['companytypeid'])
        pt = pd.merge(pt, country_ref, left_on=['companyid'], right_on=['companyid'], how ='inner')
        pt = pt.query('countryid == 213 and incorporationcountryid == 213')
        pt = pt.drop(columns=['countryid', 'incorporationcountryid', 'CusipSedol', 'simpleindustryid']).reset_index(drop=True)
        _len_pt_5 = len(pt)
        print(f'data shrinking by ciqUS and everything above is {1 - _len_pt_5/_len_pt}')


    # analysis
    num_distinct_analysis = len(pt['AMASKCD'].unique())
    num_distinct_companies = len(pt['CUSIP'].unique())
    num_of_records = len(pt)

    print('some selective statistics:')
    print('-----------------------')
    print('number of records: ' + str(num_of_records))
    print('the number of distinct analysts: ' + str(num_distinct_analysis))
    print('the number of distinct companies: ' + str(num_distinct_companies))

    pt.to_parquet('IBES_clean_parquet/pt.parquet')
    pt.to_csv('IBES_clean_csv/pt.csv')

# console output

# recommend

# /Users/zhenggong/Documents/GitHub/IBES_selected/runnables/recommend_tp_etl.py:27: DtypeWarning: Columns (4) have mixed types. Specify dtype option on import or set low_memory=False.
#   recommend = pd.read_csv('/Users/zhenggong/Documents/GitHub/IBES_selected/IBES_csv/nahghdromygr63ao.csv', index_col=[0])
# data shrinking by dropping time cutoff data is 0.47422250311227876
# data shrinking by time cutoff data and US data is 0.8771556826773999
# data shrinking by time cutoff data and US data and CUSIP to CIQcompanyid matching is 0.8944132367954094
# data shrinking by ciqUS and everything above is 0.9016131660212985
# some selective statistics:
# -----------------------
# number of records: 309170
# the number of distinct analysts: 8188
# the number of distinct companies: 9273
# ====================

# pt

# data shrinking by time cutoff data is 0.1651499383887286
# data shrinking by dropping time cutoff data and US data is 0.7560593231045499
# data shrinking by time cutoff data and US data and CUSIP to CIQcompanyid matching is 0.7813679817651791
# data shrinking by ciqUS and everything above is 0.7937143281903445
# some selective statistics:
# -----------------------
# number of records: 1404227
# the number of distinct analysts: 8207
# the number of distinct companies: 9091