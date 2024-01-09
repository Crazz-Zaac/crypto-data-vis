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
    def __init__(self, f_name, period = 100):
        self.period = period
        self.f_name = f_name
        self.clean_dataset_path = DATASET_DIR + '/' + 'raw_data/'
        self.indicators = ["MA", "EMA", "SMA", "WMA", "RSI", "MOM", "DEMA", "TEMA"]
        self.stock_data = pd.read_csv(self.clean_dataset_path + self.f_name.lower()+ '.csv')
        self.stock_data['Date'] = pd.to_datetime(self.stock_data['Timestamp'], unit='ms')
        
        # Calculate Simple Moving Average (SMA) with a window of 3 periods
        self.stock_data['SMA'] = talib.SMA(self.stock_data['Close'], timeperiod=self.period)

        # Calculate Exponential Moving Average (EMA) with a window of self.period periods
        self.stock_data['EMA'] = talib.EMA(self.stock_data['Close'], timeperiod=self.period)

        # Calculate Relative Strength Index (RSI) with a window of self.period periods
        self.stock_data['RSI'] = talib.RSI(self.stock_data['Close'])

        # Calculate Double Exponential Moving Average (DEMA) with a window of self.period periods
        self.stock_data['DEMA'] = talib.DEMA(self.stock_data['Close'], timeperiod=self.period)

        # Calculate Triple Exponential Moving Average (TEMA) with a window of self.period periods
        self.stock_data['TEMA'] = talib.TEMA(self.stock_data['Close'], timeperiod=self.period)
        
        # Calculate Weighted Moving Average (WMA) with a window of self.period periods
        self.stock_data['WMA'] = talib.WMA(self.stock_data['Close'], timeperiod=self.period)

        # Calculate Momentum (MOM) with a window of self.period periods
        self.stock_data['MOM'] = talib.MOM(self.stock_data['Close'], timeperiod=self.period)

        # Calculate Moving Average (MA) with a window of self.period periods
        self.stock_data['MA'] = talib.MA(self.stock_data['Close'], timeperiod=self.period)
        
        self.stock_data['LinearReg'] = talib.LINEARREG(self.stock_data['Close'], timeperiod=self.period)
 
    
    
    def candleStick(self):
        df = self.stock_data.copy()
        # df = df.dropna()
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
            height=600,  # Adjust the height as needed
            width=800,
            plot_bgcolor='#e3ebf3',
            xaxis=dict(showgrid=True, gridwidth=1, gridcolor='lightgrey'),  # Show x-axis gridlines
            yaxis=dict(showgrid=True, gridwidth=1, gridcolor='lightgrey'),  # Show y-axis gridlines
        )
        fig.update_xaxes(title_text="Date")
        fig.update_yaxes(title_text="Price ($)")

        st.plotly_chart(fig)
    
    def volatilityMetrics(self):
        df = self.stock_data.copy()
        df['ATR'] = df['High'] - df['Low']
        df['ATR'] = df['ATR'].ewm(span=14, adjust=False).mean()
        
        # Calculate rolling standard deviation for volatility
        df['Volatility'] = df['Close'].rolling(window=14).std()
        
        df['Date'] = pd.to_datetime(df['Date'])  # Convert 'Date' column to datetime if needed
        df.set_index('Date', inplace=True)  # Set 'Date' as the index

        # Plotting
        plt.figure(figsize=(10, 6))

        # Plot ATR
        plt.plot(df.index, df['ATR'], label='ATR', color='blue')

        # Plot Volatility (rolling standard deviation)
        plt.plot(df.index, df['Volatility'], label='Volatility', color='red')

        plt.title('Volatility Metrics - ATR and Volatility (Rolling Std)')
        plt.xlabel('Date')
        plt.ylabel('Value')
        plt.legend()
        plt.grid()

        st.pyplot(plt)
    
    def simpleMovingAverage(self):
        df = self.stock_data.copy()
        df['Date'] = pd.to_datetime(df['Date'])  # Convert 'Date' column to datetime if needed
        df.set_index('Date', inplace=True)  # Set 'Date' as the index

        # Calculating EMA (assuming 'EMA' column exists in your DataFrame)
        # Replace 'EMA' with the actual column name if it differs
        fig = go.Figure(data=[
            go.Scatter(x=df.index, y=df['Close'], mode='lines', name='Close Price'),
            go.Scatter(x=df.index, y=df['SMA'], mode='lines', name='SMA', line=dict(color='orange'))
        ])

        # Setting up layout and title
        fig.update_layout(
            title='Simple Moving Average with timeperiod = 100',
            xaxis=dict(title='Date'),
            yaxis=dict(title='Price'),
            height=600,  # Adjust the height as needed
            width=800    # Adjust the width as needed
        )

        # Display the plot
        st.plotly_chart(fig)
    
    def exponentialMovingAverage(self):
        df = self.stock_data.copy()
        df['Date'] = pd.to_datetime(df['Date'])  # Convert 'Date' column to datetime if needed
        df.set_index('Date', inplace=True)  # Set 'Date' as the index

        # Calculating EMA (assuming 'EMA' column exists in your DataFrame)
        # Replace 'EMA' with the actual column name if it differs
        fig = go.Figure(data=[
            go.Scatter(x=df.index, y=df['Close'], mode='lines', name='Close Price'),
            go.Scatter(x=df.index, y=df['EMA'], mode='lines', name='EMA', line=dict(color='red'))
        ])

        # Setting up layout and title
        fig.update_layout(
            title='Exponential Moving Average with timeperiod = 100',
            xaxis=dict(title='Date'),
            yaxis=dict(title='Price'),
            height=600,  # Adjust the height as needed
            width=800    # Adjust the width as needed
        )

        # Display the plot
        st.plotly_chart(fig)
    
    

    def relativeStrengthIndex(self):
        df = self.stock_data.copy()
        df['Date'] = pd.to_datetime(df['Date'])  # Convert 'Date' column to datetime if needed
        df.set_index('Date', inplace=True)  # Set 'Date' as the index

        # Creating a figure with two vertically stacked subplots
        fig = go.Figure()

        # Adding two subplots with shared x-axis
        fig.add_trace(go.Scatter(x=df.index, y=df['Close'], mode='lines', name='Close Price', yaxis='y1'))

        fig.add_trace(go.Scatter(x=df.index, y=df['RSI'], mode='lines', name='RSI', yaxis='y2'))

        # Setting up layout for the subplots
        fig.update_layout(
            xaxis=dict(title='Date'),
            yaxis=dict(title='Close Price', side='left', showgrid=False, domain=[0.4, 1]),
            yaxis2=dict(title='RSI', overlaying='y', side='right', showgrid=False, range=[0, 100], domain=[0, 0.35]),
            title='Stock Prices and RSI',
            height=600,  # Adjust the height as needed
            width=800    # Adjust the width as needed
        )

        # Display the plot
        st.plotly_chart(fig)
    
    def linearRegression(self):
        df = self.stock_data.copy()
        df['Date'] = pd.to_datetime(df['Date'])  # Convert 'Date' column to datetime if needed
        df.set_index('Date', inplace=True)  # Set 'Date' as the index

        fig = go.Figure(data=[
            go.Scatter(x=df.index, y=df['Close'], mode='lines', name='Close Price'),
            go.Scatter(x=df.index, y=df['LinearReg'], mode='lines', name='Linear Regression', line=dict(color='green'))
        ])

        # Setting up layout and title
        fig.update_layout(
            title='Linear Regression with timeperiod = 100',
            xaxis=dict(title='Date'),
            yaxis=dict(title='Price'),
            height=600,  # Adjust the height as needed
            width=800    # Adjust the width as needed
        )

        # Display the plot
        st.plotly_chart(fig)

      
    def movingAverageConvergenceDivergence(self):
        df = self.stock_data.copy()

        # Calculate MACD, Signal line, and Histogram using pandas_ta
        macd, macd_signal, macd_hist = talib.MACD(df['Close'])
        hist_colors = ['red' if c1 < 0 else 'green' for c1 in macd_hist]

        # Create a Matplotlib figure and subplots
        fig, axs = plt.subplots(2, 1, gridspec_kw={'height_ratios': [3, 1]}, figsize=(10, 6))

        # Plot Close prices
        axs[0].plot(df['Close'])
        axs[0].set_ylabel('Close Price')

        # Plot MACD and Signal line
        axs[1].plot(macd, 'b-', label='MACD')
        axs[1].plot(macd_signal, '--', color='orange', label='Signal Line')
        axs[1].legend()

        # Plot histogram with dynamically colored bars
        axs[1].bar(macd_hist.index, macd_hist, color=hist_colors)

        # Setting titles and labels
        axs[0].set_title('Moving Average Convergence Divergence (MACD)')
        axs[1].set_xlabel('Index')
        axs[1].set_ylabel('MACD')

        # Adjust layout
        plt.tight_layout()

        # Display the plot
        st.pyplot(plt)
    

        
    # def volumeAnalysis(self):
        
 
    


#Dashboard

# symbol = 'ETHUSDT'
# f_path = DATASET_DIR + '/processed_data/' + symbol.lower() + '.csv'


# data_visualizer = DataVis(f_name=symbol)
# fig = data_visualizer.candleStick()

# st.plotly_chart(fig)

# # data_visualizer.volatilityMetrics()
# data_visualizer.simpleMovingAverage()
# data_visualizer.exponentialMovingAverage()
# data_visualizer.relativeStrengthIndex()
# data_visualizer.linearRegression()
# data_visualizer.movingAverageConvergenceDivergence()






 # def movingAverageConvergenceDivergence(self):
    #     df = self.stock_data.copy()
    #     df['Date'] = pd.to_datetime(df['Date'])  # Convert 'Date' column to datetime if needed
    #     df.set_index('Date', inplace=True)  # Set 'Date' as the index

    #     # Calculate MACD, Signal line, and Histogram using pandas_ta
    #     macd, macd_signal, macd_hist = talib.MACD(df['Close'])
    #     hist_colors = ['red' if c1 < 0 else 'green' for c1 in macd_hist]

    #     # Create a Plotly figure
    #     fig = go.Figure()

    #     # Adding traces for Close prices, MACD line, Signal line, and Histogram
    #     fig.add_trace(go.Scatter(x=df.index, y=df['Close'], mode='lines', name='Close Price'))
    #     fig.add_trace(go.Scatter(x=df.index, y=macd, mode='lines', name='MACD', line=dict(color='#A12FF8')))
    #     fig.add_trace(go.Scatter(x=df.index, y=macd_signal, mode='lines', name='Signal Line', line=dict(color='olivedrab')))  # Hex color for FF1493 (DeepPink)
    #     fig.add_trace(go.Bar(x=df.index, y=macd_hist, name='MACD Histogram', marker_color=hist_colors))


    #     # Setting up layout and title
    #     fig.update_layout(
    #         title='Moving Average Convergence Divergence (MACD)',
    #         xaxis=dict(title='Date'),
    #         yaxis=dict(title='Price'),
    #         height=400,  # Adjust the height as needed
    #         width=800    # Adjust the width as needed
    #     )
    #     # fig.update_xaxes(range=['2022-01-01', '2023-01-01'])
    #     # Display the plot
    #     st.plotly_chart(fig)