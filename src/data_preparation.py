import requests
from configparser import ConfigParser
import csv, os
import time
import pandas as pd
from settings import CONFIG_DIR, DATASET_DIR
import streamlit as st

class DataPreparation:
    def __init__(self, symb, start, end):
        self.url = 'https://api.binance.com/api/v3/klines'
        self.interval = '1d'
        self.symbol = symb
        self.start_time = start
        self.end_time = end
        
    def getData(self):
        start_exec_time = time.time() # start execution time
        
        config = ConfigParser()
        config_path = CONFIG_DIR + '/' + 'config.ini' 
        config.read(config_path)
        api_key = config.get('API', 'api_key')
        
        directory_path = DATASET_DIR + '/raw_data/' 
        
        params = {
            'symbol': self.symbol,
            'interval': self.interval,
            'startTime': self.start_time,
            'endTime': self.end_time,
            'limit': 1000  # Maximum limit per request
        }
        print(params)
        
        headers = {
            'X-MBX-APIKEY': api_key
        }
        
        response = requests.get(self.url, headers=headers, params=params)
        
        if response.status_code == 200:
            data = response.json()
            
            
            file_path = os.path.join(directory_path, f"{self.symbol.lower()}.csv")
            
            # checking if the file already exists to delete it and creat a new one
            if os.path.exists(file_path):
                os.remove(file_path)

            with open(file_path, mode='w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(["Timestamp", "Open", "High", "Low", "Close", "Volume", "Date"])
                
                for candlestick in data:
                    timestamp = candlestick[0]
                    open_price = candlestick[1]
                    high_price = candlestick[2]
                    low_price = candlestick[3]
                    close_price = candlestick[4]
                    volume = candlestick[5]
                    date = pd.to_datetime(timestamp, unit='ms')
                    # Writing each candlestick data as a row in the CSV file
                    writer.writerow([timestamp, open_price, high_price, low_price, close_price, volume, date])
            
            # df = pd.read_csv(file_path)
            # df['Date'] = pd.to_datetime(df['Timestamp'], unit='ms')
            
            end_exec_time = time.time()
            execution_time = end_exec_time - start_exec_time
            st.success(f"Retrieved {len(data)} candlesticks for {self.symbol} in given date. \nData saved as {self.symbol.lower()}.csv")
            st.write(f"Total execution time: {execution_time:.2f} seconds")
        else:
            raise Exception("Failed to fetch and save data")
