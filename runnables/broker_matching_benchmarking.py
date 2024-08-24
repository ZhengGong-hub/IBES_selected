import pandas as pd 

overall = pd.read_parquet('data/overall.parquet')
print(overall
      )

overall['confidence_on_distance'] = overall['confidence_on_distance'].abs()

overall = overall.query('total_valid_record >= 5')

overall = overall.query('confidence_on_distance > 0.2 and confidence_on_density > 0.2')

overall['overall_confidence'] = overall['confidence_on_density'] ** 0.5 * overall['confidence_on_distance'] ** 0.5

overall['correct'] = True

overall = overall.sort_values(by='overall_confidence', ascending=False)

print(overall.head(700))

overall.to_csv('data/overall_shortened.csv')