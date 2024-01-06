import pandas as pd
import numpy as np
import os, glob, talib
import csv
from settings import DATASET_DIR



class DataClean:
    def __init__(self, symbol):
        self.symbol = symbol
        self.raw_dataset_path = DATASET_DIR + '/' + 'raw_data/'
        self.clean_dataset_path = DATASET_DIR + '/' + 'processed_data/'
    
    @st.cache_data
    def addTechnicalIndicators(self):
        df = pd.read_csv(self.raw_dataset_path + self.symbol.lower()+ '_candlesticks.csv')
        
        df['Date'] = pd.to_datetime(df['Timestamp'], unit='ms')
        
        # Calculate Simple Moving Average (SMA) with a window of 3 periods
        df['SMA'] = talib.SMA(df['Close'], timeperiod=3)

        # Calculate Exponential Moving Average (EMA) with a window of 3 periods
        df['EMA'] = talib.EMA(df['Close'], timeperiod=3)

        # Calculate Relative Strength Index (RSI) with a window of 3 periods
        df['RSI'] = talib.RSI(df['Close'], timeperiod=3)

        # Calculate Double Exponential Moving Average (DEMA) with a window of 3 periods
        df['DEMA'] = talib.DEMA(df['Close'], timeperiod=3)

        # Calculate Triple Exponential Moving Average (TEMA) with a window of 3 periods
        df['TEMA'] = talib.TEMA(df['Close'], timeperiod=3)
        
        # Calculate Weighted Moving Average (WMA) with a window of 3 periods
        df['WMA'] = talib.WMA(df['Close'], timeperiod=3)

        # Calculate Momentum (MOM) with a window of 3 periods
        df['MOM'] = talib.MOM(df['Close'], timeperiod=3)

        # Calculate Moving Average (MA) with a window of 3 periods
        df['MA'] = talib.MA(df['Close'], timeperiod=3)
        
        
        output_filename = self.symbol.lower() + '_technical_indicators.csv'
        output_path = self.clean_dataset_path + output_filename
        df.to_csv(output_path, index=False) 

def main():
    symbol = 'ETHUSDT'
    
    DataClean(symbol).addTechnicalIndicators()

if __name__ == '__main__':
    main()