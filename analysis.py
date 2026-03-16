import pandas as pd
import numpy as np

#Data Ingestion

df = pd.read_csv(r"C:\Users\venne\Downloads\New Afficionado Coffee Roasters.csv")
print(df.head())

pd.set_option('display.max_rows', 149118)
pd.set_option('display.max_columns', 11)
df

