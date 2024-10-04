import pandas as pd
import glob
from fastparquet import write

parquet_directory = 'partitions/'

all_parquet_files = glob.glob(f"{parquet_directory}/*.parquet")

dataframes = [pd.read_parquet(file) for file in all_parquet_files]
combined_df = pd.concat(dataframes, ignore_index=True)

combined_df = combined_df.sort_values(by='time')

output_parquet_file = 'stars.parquet'
write(output_parquet_file, combined_df, write_index=False)

print(f"Data successfully written to {output_parquet_file}")
