import pandas as pd
import numpy as np
import psycopg2 as psycopg
import os
from dotenv import load_dotenv

"""Extract Raw From The CSV File"""
df = pd.read_csv('main_data.csv')

 
"""Transfrom Extracted Data"""

df.columns = ['datetime', 'location', 'customer', 'order', 'price', 'payment_method', 'card_number']


df[['date', 'time']] = df['datetime'].str.split(' ', expand=True)
df.drop(columns=['datetime'], inplace=True)

# Move date and time to the front
cols = ['date', 'time'] + [col for col in df.columns if col not in ['date', 'time']]
df = df[cols]


df['customer'] = df['customer'].str.replace('.', '', regex=False)

# Replace '-' with ',' to help split multiple orders
df['order'] = df['order'].str.replace('-', ',', regex=False)

def split_orders(order_str):
    if pd.isna(order_str):
        return {}
    orders = [item.strip() for item in order_str.split(',')]
    result = {}
    for i, item in enumerate(orders, 1):
        if ' - ' in item:
            name, price = item.rsplit(' - ', 1)
            result[f'order_{i}'] = name.strip()
            result[f'price_{i}'] = float(price.strip())
    return pd.Series(result)

order_split_df = df['order'].apply(split_orders)
df = pd.concat([df.drop(columns=['order']), order_split_df], axis=1)


df['masked_card_number'] = df['card_number'].astype(str).apply(
    lambda x: 'X' * (len(x) - 4) + x[-4:] if x != 'nan' else None
)
df.drop(columns=['card_number'], inplace=True)


df = df.drop_duplicates()


print("Null values per column:\n", df.isnull().sum())


print(df)



"""Load Transformed Data Into Database Using psycopg2"""
df.to_csv('cleaned_orders.csv', index=False)
print('Cleaned data saved to ', 'cleaned_orders.csv')

# Connect to Database
load_dotenv()
host_name = os.environ.get("POSTGRES_HOST")
database_name = os.environ.get("POSTGRES_DB")
user_name = os.environ.get("POSTGRES_USER")
user_password = os.environ.get("POSTGRES_PASSWORD")

with psycopg.connect(
            host=host_name,
            dbname=database_name,
            user=user_name,
            password=user_password) as connection:
            cursor = connection.cursor()
    
cursor = connection.cursor()
create_table_query = """
CREATE TABLE IF NOT EXISTS orders (
date DATE,
time TIME,
location TEXT,
customer TEXT,
payment_method TEXT,
price NUMERIC,
order_1 TEXT,
price_1 NUMERIC,
order_2 TEXT,
price_2 NUMERIC,
order_3 TEXT,
price_3 NUMERIC,
masked_card_number TEXT
);"""

cursor.execute(create_table_query)

cursor.execute("DELETE FROM orders")


for _, row in df.iterrows():
    cursor.execute("""
        INSERT INTO orders (
            date, time, location, customer, payment_method, price,
            order_1, price_1, order_2, price_2, order_3, price_3, masked_card_number
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        row.get('date'), row.get('time'), row.get('location'), row.get('customer'),
        row.get('payment_method'), row.get('price'),
        row.get('order_1'), row.get('price_1'),
        row.get('order_2'), row.get('price_2'),
        row.get('order_3'), row.get('price_3'),
        row.get('masked_card_number')
    ))

connection.commit()
cursor.close()
connection.close()

print("Data successfully loaded into PostgreSQL.")