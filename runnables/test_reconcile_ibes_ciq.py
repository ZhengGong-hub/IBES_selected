import pandas as pd 

ciq = pd.read_csv('/Users/zhenggong/Documents/GitHub/et_explorer/output/analyst_coverage.csv', index_col=[0])
print(ciq)

ibes = pd.read_csv('data/analyst_stat.csv', index_col=[0]).reset_index()
print(ibes)

df = pd.merge(ciq, ibes, left_on=['Transformed Names'], right_on=['ANALYST'], how='inner')
print(df)

df.to_csv('data/ibes_ciq_reconcile.csv')

# wow! surprisingly high!