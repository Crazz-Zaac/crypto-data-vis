import csv, requests
from datetime import datetime
import pandas as pd
import streamlit as st
from bokeh.plotting import figure, column
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import talib
from settings import DATASET_DIR

class DataVis:
    def __init__(self, f_name):
        self.f_name = f_name
        self.clean_dataset_path = DATASET_DIR + '/' + 'processed_data/'
        self.indicators = ["MA", "EMA", "SMA", "WMA", "RSI", "MOM", "DEMA", "TEMA"]
    
    def candleStick(self):
        df = pd.read_csv(self.clean_dataset_path + self.f_name.lower()+ '_technical_indicators.csv')
        df = df.dropna()
        df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m-%d')
        
        df['MA5'] = df['Close'].rolling(5).mean()
        fig = go.Figure(data = [go.Candlestick(x=df['Date'],
                                            open=df['Open'],
                                            high=df['High'],
                                            low=df['Low'],
                                            close=df['Close'],
                                            increasing_fillcolor='#12c783',  # Color for increasing candles (close > open)
                                            decreasing_fillcolor='#ee455c'),  # Color for decreasing candles (close < open)
                            go.Scatter(x=df['Timestamp'], y=df['MA5'], line=dict(color='blue', width=2), name='5-day Moving Average'),
                            go.Scatter(x=df['Timestamp'], y=df['Close'], line=dict(color='#512ff8', width=2), name='Close'),
                            go.Scatter(x=df['Timestamp'], y=df['MA'], line=dict(color='#3d8ccc', width=2), mode='lines', name='MA'),
                            go.Scatter(x=df['Timestamp'], y=df['EMA'], line=dict(color='#6A5ACD', width=2), mode='lines', name='EMA'),
                            go.Scatter(x=df['Timestamp'], y=df['WMA'], line=dict(color='#7CFC00', width=2), mode='lines', name='WMA'),
                            go.Scatter(x=df['Timestamp'], y=df['DEMA'], line=dict(color='#00FFFF', width=2), mode='lines', name='DEMA'),
                            go.Scatter(x=df['Timestamp'], y=df['TEMA'], line=dict(color='#FFA500', width=2), mode='lines', name='TEMA'),
                            go.Scatter(x=df['Timestamp'], y=df['RSI'], line=dict(color='#A12FF8', width=1), mode='lines', name='RSI'),
                            go.Scatter(x=df['Timestamp'], y=df['MOM'], line=dict(color='#FF1493', width=1), mode='lines', name='MOM')                            
                            ])
        
        fig.update_layout(
            title= self.f_name + ' Stock Price Analysis',
            height=800,
            plot_bgcolor='#e3ebf3',
            xaxis=dict(showgrid=True, gridwidth=1, gridcolor='lightgrey'),  # Show x-axis gridlines
            yaxis=dict(showgrid=True, gridwidth=1, gridcolor='lightgrey'),  # Show y-axis gridlines
        )
        fig.update_xaxes(title_text="Date")
        fig.update_yaxes(title_text="Price ($)")

        return fig
    
    def volatilityMetrics(self):
        stock_data = pd.read_csv(self.clean_dataset_path + self.f_name.lower()+ '_technical_indicators.csv')
        stock_data['ATR'] = stock_data['High'] - stock_data['Low']
        stock_data['ATR'] = stock_data['ATR'].ewm(span=14, adjust=False).mean()
        
        # Calculate rolling standard deviation for volatility
        stock_data['Volatility'] = stock_data['Close'].rolling(window=14).std()
        
        stock_data['Date'] = pd.to_datetime(stock_data['Date'])  # Convert 'Date' column to datetime if needed
        stock_data.set_index('Date', inplace=True)  # Set 'Date' as the index

        # Plotting
        plt.figure(figsize=(10, 6))

        # Plot ATR
        plt.plot(stock_data.index, stock_data['ATR'], label='ATR', color='blue')

        # Plot Volatility (rolling standard deviation)
        plt.plot(stock_data.index, stock_data['Volatility'], label='Volatility', color='red')

        plt.title('Volatility Metrics - ATR and Volatility (Rolling Std)')
        plt.xlabel('Date')
        plt.ylabel('Value')
        plt.legend()
        plt.grid()

        st.pyplot(plt)
    
    # def volumeAnalysis(self):
        
 
    


talib_indicators = ["MA", "EMA", "SMA", "WMA", "RSI", "MOM", "DEMA", "TEMA"]

#Dashboard
st.header(":green[Candle]:red[stick] Technical Analysis")
symbol = 'ETHUSDT'
f_path = DATASET_DIR + '/processed_data/' + symbol.lower() + '_technical_indicators.csv'


data_visualizer = DataVis(f_name=symbol)
fig = data_visualizer.candleStick()

st.plotly_chart(fig)

data_visualizer.volatilityMetrics()




    