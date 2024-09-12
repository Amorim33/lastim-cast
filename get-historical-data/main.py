import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

from lib.collections import Collections, interval_historical_collections
from lib.database import db

# Function to get data for a single day
def get_intraday_data(ticker, start_date, interval):
    data = yf.download(ticker, start=start_date, end=start_date + timedelta(days=1), interval=interval)
    return data

# Function to get the historical data based on the target interval
def download_historical_data(ticker, start_date, end_date, interval):
    all_data = pd.DataFrame()

    if interval == '1d':
        return yf.download(ticker, start=start_date, end=end_date, interval=interval)

    current_date = start_date
    while current_date <= end_date:
        print(f"Downloading data for {current_date.strftime('%Y-%m-%d')}")
        try:
            daily_data = get_intraday_data(ticker, current_date, interval)
            if not daily_data.empty:
                daily_data['Date'] = current_date.strftime('%Y-%m-%d')
                all_data = pd.concat([all_data, daily_data], axis=0)
        except Exception as e:
            print(f"Error retrieving data for {current_date}: {e}")
        
        current_date += timedelta(days=1)

    return all_data

# Function to insert data into MongoDB time series
def insert_data_to_mongo(collection, data):
    if Collections[collection] is None:
        raise Exception('Invalid collection')

    # Prepare the data to be inserted
    records = []
    for index, row in data.iterrows():
        record = {
            "Datetime": index, 
            "Open": row['Open'],
            "High": row['High'],
            "Low": row['Low'],
            "Close": row['Close'],
            "Adj Close": row['Adj Close'],
            "Volume": row['Volume'],
        }
        records.append(record)
    
    if len(records):
        lastInsertedItem = db[collection].find_one(sort=[("Datetime", -1)])
        to_insert_records = []
        if lastInsertedItem:
            to_insert_records = [record for record in records if record["Datetime"] > lastInsertedItem["Datetime"]]
        else:
            to_insert_records = records

        db[collection].insert_many(to_insert_records)
        print(f"Inserted {len(records)} records in {collection}")

if __name__ == "__main__":
    ticker = "^BVSP" 
    start_date = None
    end_date = datetime.now()
    interval = input('Enter the target interval (the available intervals are: 1d, 60m, 1m): ')

    if interval == '60m':
        start_date = end_date - timedelta(days=730)
    elif interval == '1m':
        start_date = end_date - timedelta(days=30)
    elif interval == '1d':
        start_date = datetime(1993, 4, 27)
    else:
        raise Exception('Invalid interval')

    all_data = download_historical_data(ticker, start_date, end_date, interval)
    
    # Save data to MongoDB
    print("Inserting data to MongoDB")
    insert_data_to_mongo(interval_historical_collections[interval], all_data)

    # Convert timezone-aware datetime to timezone-naive
    all_data.index = all_data.index.tz_localize(None)
    all_data.to_excel(f"../assets/bvsp_data_{interval}_interval.xlsx")
    print(f"Data successfully saved to 'bvsp_data_{interval}_interval.xlsx'")
