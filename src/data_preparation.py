import requests
from configparser import ConfigParser  # Use ConfigParser, not Configparser
import csv
import os

class DataPreparation:
    def __init__(self, symb, start, end):
        # Binance API endpoint for historical kline/candlestick data
        self.url = 'https://api.binance.com/api/v3/klines'
        self.interval = '1d'
        self.symbol = symb
        self.start_time = start
        self.end_time = end
        
    
    def getData(self):
        current_dir = os.path.dirname(os.path.abspath(__file__)).replace('src', '')
        config = ConfigParser()
        config_path = os.path.join(current_dir, 'config/config.ini')
        config.read(config_path)
        api_key = config.get('API', 'api_key')
        # if config.has_section('API'):
        #     api_key = config.get('API', 'api_key')
        # else:
        #     print("File not found")
        
        directory_path = os.path.join(current_dir, 'data/raw_data/')
        
        params = {
            'symbol': self.symbol,
            'interval': self.interval,
            'startTime': self.start_time,
            'endTime': self.end_time,
            'limit': 1000  # Maximum limit per request
        }
        
        headers = {
            'X-MBX-APIKEY': api_key
        }
        response = requests.get(self.url, headers = headers, params = params)
        
        if response.status_code == 200:
            print(self.symbol)
            data = response.json()
            file_path = os.path.join(directory_path, f"{self.symbol.lower()}_candlesticks.csv")

            #writing data to CSV file
            with open(file_path, mode='w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(["Timestamp", "Open", "High", "Low", "Close", "Volume"])
                
                for candlestick in data:
                    timestamp = candlestick[0]
                    open_price = candlestick[1]
                    high_price = candlestick[2]
                    low_price = candlestick[3]
                    close_price = candlestick[4]
                    volume = candlestick[5]
                    
                    writer.writerow([timestamp, open_price, high_price, low_price, close_price, volume])
        
        else:
            raise Exception("Failed to fetch and save data")
          