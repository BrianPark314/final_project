import sqlite3
import pandas as pd


metge_df_tv = pd.read_csv('merge_df_tv.csv')
metge_df_tv.columns = metge_df_tv.columns.str.strip()
connection = sqlite3.connect('info.db')

metge_df_tv.to_sql('info',connection,if_exists='replace')

connection.close()