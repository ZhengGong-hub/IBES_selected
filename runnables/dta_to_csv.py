import pandas as pd 
import glob

dta_file_paths = glob.glob('IBES_extracted/*')

for dta_file in dta_file_paths:

    output_file_path = dta_file.replace('.dta', '.csv').replace('IBES_extracted/', 'IBES_csv/')
    print(output_file_path)

    data = pd.io.stata.read_stata(dta_file)
    print(data)
    data.to_csv(output_file_path)
