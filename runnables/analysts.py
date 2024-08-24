import pandas as pd 

rec = pd.read_csv('IBES_clean_csv/recommendation.csv', index_col=[0])
rec = rec.query("ANALYST >= 'A'") # clean up dirty analyst name
rec['ANALYST'] = rec['ANALYST'].apply(lambda x: ' '.join(x.split()))
rec['ANALYST'] = rec['ANALYST'].apply(lambda x: x.replace(',CFA', ''))
rec['ANALYST'] = rec['ANALYST'].apply(lambda x: x.replace(',CF', '')) # sometimes it is not given in full
rec['ANALYST'] = rec['ANALYST'].apply(lambda x: x.replace(', CFA', ''))
rec['ANALYST'] = rec['ANALYST'].apply(lambda x: x.replace(', PHD', ''))
rec['ANALYST'] = rec['ANALYST'].apply(lambda x: x.replace(', PH.D.', ''))
rec['ANALYST'] = rec['ANALYST'].apply(lambda x: x.replace(', DPHIL', ''))
# print(rec)

# df = rec.drop_duplicates(subset=['AMASKCD', 'ANALYST'])
# df = df[df.duplicated(subset=['ANALYST'])]

# print(df)
# assert False

tp = pd.read_csv('IBES_clean_csv/pt.csv', index_col=[0]).rename(columns={'ALYSNAM':'ANALYST'})
tp = tp.query("ANALYST >= 'A'") # clean up dirty analyst name
tp['ANALYST'] = tp['ANALYST'].apply(lambda x: ' '.join(x.split()))
tp['ANALYST'] = tp['ANALYST'].apply(lambda x: x.replace(',CFA', ''))
tp['ANALYST'] = tp['ANALYST'].apply(lambda x: x.replace(',CF', '')) # sometimes it is not given in full
tp['ANALYST'] = tp['ANALYST'].apply(lambda x: x.replace(', CFA', ''))
tp['ANALYST'] = tp['ANALYST'].apply(lambda x: x.replace(', PHD', ''))
tp['ANALYST'] = tp['ANALYST'].apply(lambda x: x.replace(', PH.D.', ''))
tp['ANALYST'] = tp['ANALYST'].apply(lambda x: x.replace(', DPHIL', ''))
# print(tp)

rec_grouped_analyst = rec.groupby(by=['AMASKCD']).count()[['CUSIP']].rename(columns={'CUSIP' : 'COUNT_RECOM'})
rec_grouped_analyst_co = rec.groupby(by=['AMASKCD', 'ESTIMID']).count()[['CUSIP']].rename(columns={'CUSIP' : 'COUNT_RECOM'})
rec_grouped_analyst_coverage = rec.groupby(by=['AMASKCD', 'TICKER']).count()[['CUSIP']].rename(columns={'CUSIP' : 'COUNT_RECOM'})
rec_grouped_analyst_co_coverage = rec.groupby(by=['AMASKCD', 'ESTIMID', 'TICKER']).count()[['CUSIP']].rename(columns={'CUSIP' : 'COUNT_RECOM'})
# print(rec_grouped)

tp_grouped_analyst = tp.groupby(by=['AMASKCD']).count()[['CUSIP']].rename(columns={'CUSIP' : 'COUNT_TP'})
tp_grouped_analyst_co = tp.groupby(by=['AMASKCD', 'ESTIMID']).count()[['CUSIP']].rename(columns={'CUSIP' : 'COUNT_TP'})
tp_grouped_analyst_coverage = tp.groupby(by=['AMASKCD', 'TICKER']).count()[['CUSIP']].rename(columns={'CUSIP' : 'COUNT_TP'})
tp_grouped_analyst_co_coverage = tp.groupby(by=['AMASKCD', 'ESTIMID', 'TICKER']).count()[['CUSIP']].rename(columns={'CUSIP' : 'COUNT_TP'})
# print(tp_grouped)

comb_grouped = pd.merge(left=rec_grouped_analyst, right=tp_grouped_analyst, left_index=True, right_index=True, how='outer').fillna(0)
print(comb_grouped.describe().astype(int))
comb_grouped.astype(int).to_csv('data/analyst_stat.csv')

comb_grouped = pd.merge(left=rec_grouped_analyst_co, right=tp_grouped_analyst_co, left_index=True, right_index=True, how='outer').fillna(0)
print(comb_grouped.describe().astype(int))
comb_grouped.astype(int).to_csv('data/analyst_broker_stat.csv')

comb_grouped = pd.merge(left=rec_grouped_analyst_coverage, right=tp_grouped_analyst_coverage, left_index=True, right_index=True, how='outer').fillna(0)
print(comb_grouped.describe().astype(int))
comb_grouped.astype(int).to_csv('data/analyst_coverage_stat.csv')

comb_grouped = pd.merge(left=rec_grouped_analyst_co_coverage, right=tp_grouped_analyst_co_coverage, left_index=True, right_index=True, how='outer').fillna(0)
print(comb_grouped.describe().astype(int))
comb_grouped.astype(int).to_csv('data/analyst_broker_coverage_stat.csv')

