import numpy as np
import pandas as pd
import pyodbc
import requests

server = 'discog-scrapes.database.windows.net'
database = 'discog-scrapes'
username = 'thomas'
password = 'Wiering@1'
driver = '{ODBC Driver 18 for SQL Server}'
con = pyodbc.connect('DRIVER=' + driver + ';'
                                          'SERVER=tcp:' + server +
                     ';PORT=1433;DATABASE=' + database + ';'
                                                         'UID=' + username + ';PWD='
                     + password)

# Connect to the database and read the table into a DataFrame
df = pd.read_sql("SELECT * FROM MarketPlace", con)
df = df[df['Available']]
df = df[df['PriceCurrency'] == 'EUR']
df = df[df['ShipsFrom'].isin(['Netherlands', 'Germany', 'Belgium', 'France', 'Italy', 'Spain'])]

df['Rank'] = df.groupby('MasterId')['Price'].rank(pct=True)


result = []
for unique_seller in df['Seller'].unique():
    seller_df = df[df['Seller'] == unique_seller]
    seller_item = {'seller': unique_seller,
                   'best deals': []}
    ranks = []
    for master_id in seller_df['MasterId'].unique():
        this_master = seller_df[seller_df['MasterId'] == master_id]
        min_index = this_master['Rank'].idxmin()
        # Get the row with the minimum price
        min_row = this_master.loc[min_index]
        seller_item['best deals'].append({
            'title': min_row['Title'],
            'price': min_row['Price'],
            'Rank': min_row['Rank']
        })
        ranks.append(min_row['Rank'])
    seller_item['median rank'] = np.median(ranks)
    if len(ranks) > 1:
        result.append(seller_item)

sorted = sorted(result, key=lambda d: d['median rank'])

for i in range(len(sorted)):
    print("amount of records = {} total price = {}".format(len(sorted[i]['best deals']), sum([x['price'] for x in sorted[i]['best deals']])))
    print("average ppr = {}".format(sum([x['price'] for x in sorted[i]['best deals']])/len(sorted[i]['best deals'])))
    print(sorted[i])

