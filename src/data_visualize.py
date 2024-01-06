import csv
import requests
import pandas as pd
import plotly.graph_objects as go
import datetime
import streamlit as st

class DataVis:
    def __init__(self):
        pass
    
    def showCandlestick():
        fig = go.Figure(data = [go.Candlestick(x=df['Date'],
                                      open=df['Open'],
                                      high=df['High'],
                                       low=df['Low'],
                                       close=df['Close'])])
fig.show()