import pandas as pd
import locale
locale.setlocale(locale.LC_TIME, 'en_US')
df = pd.read_csv('netflix_titles.csv')
print(df.dtypes)

df['date_added'] = pd.to_datetime(df['date_added'])

