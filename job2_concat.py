import pandas as pd
import glob

data_path = glob.glob('./crawling_data/*.csv')
df = pd.DataFrame()
for path in data_path:
    df_temp = pd.read_csv(path)
    df = pd.concat([df, df_temp], ignore_index=True)
df.drop_duplicates(inplace=True)
df.dropna(inplace=True)
df.reset_index(inplace=True, drop=True)
df.info()
df.to_csv('./crawling_data_2/crawling_data_concat_1.csv', index=False)