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
    
    def addTechnicalIndicators(self):
        df = pd.read_csv(self.raw_dataset_path + self.symbol.lower()+ '_candlesticks.csv')
        # Calculate Simple Moving Average (SMA) with a window of 14 periods
        df['SMA_14'] = talib.SMA(df['Close'], timeperiod=14)

        # Calculate Exponential Moving Average (EMA) with a window of 12 periods
        df['EMA_12'] = talib.EMA(df['Close'], timeperiod=12)

        # Calculate Relative Strength Index (RSI) with a window of 14 periods
        df['RSI_14'] = talib.RSI(df['Close'], timeperiod=14)

        # Calculate Double Exponential Moving Average (DEMA) with a window of 12 periods
        df['DEMA_12'] = talib.DEMA(df['Close'], timeperiod=12)

        # Calculate Triple Exponential Moving Average (TEMA) with a window of 12 periods
        df['TEMA_12'] = talib.TEMA(df['Close'], timeperiod=12)
        
        print(df.head())

def main():
    symbol = 'ETHUSDT'
    
    DataClean(symbol).addTechnicalIndicators()

if __name__ == '__main__':
    main()