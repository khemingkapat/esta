import pandas as pd

df = pd.read_parquet(
    "./parsed/9e8d6ad0-1048-4909-8327-3eb857671aa2/bomb_events_2aa88ea8-3e89-4f63-a3c1-9cd90d041eae.parquet"
)
print(df.columns)
