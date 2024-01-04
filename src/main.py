import streamlit as st
import csv
import requests
import pandas as pd
import plotly.graph_objects as go
import datetime

# from secret import api_key, secret_key
from symbol_extract import ExtractSymbol
from data_preparation import DataPreparation

st.title("Visualize and Explore Cryptocurriencies Data")

# Binance API endpoint for historical kline/candlestick data
url = 'https://api.binance.com/api/v3/klines'


# A selectbox to the sidebar for symbol selection
extractor = ExtractSymbol(url='https://api.binance.com/api/v3/ticker/24hr')
symbols_list = tuple(extractor.getSymbols())

crypto_symb = st.sidebar.selectbox(
    'Select a crypto symbol',
    symbols_list,
    index=None,
    placeholder="Select crypto symbol"
)

# Check if the symbols are fetched
if 'symbols_list' not in st.session_state:
    st.session_state.symbols_list = extractor.getSymbols()

# Check if crypto_symb is set in the session state, if not, set it to the first symbol
if 'crypto_symb' not in st.session_state:
    st.session_state.crypto_symb = st.session_state.symbols_list[0]


# start and end date for data
today = datetime.datetime.now()
prev_year = today.year - 1

start_year = st.sidebar.select_slider('Select start year', options=list(range(2000, prev_year + 1)))
end_year = st.sidebar.select_slider('Select end year', options=list(range(start_year, prev_year + 1)))

s_date = datetime.datetime.strptime(str(datetime.date(start_year, 1, 1)), '%Y-%m-%d')
start_date = int(s_date.timestamp())
e_date = datetime.datetime.strptime(str(datetime.date(end_year, 12, 31)), '%Y-%m-%d')
end_date = int(e_date.timestamp())

# Save the selected values to the session_state
st.session_state.crypto_symb = crypto_symb
st.session_state.start_date = start_date
st.session_state.end_date = end_date

# preparation of raw data
# st.sidebar.button("Prepare Data", type="primary")
if st.sidebar.button("Prepare Data", type="primary"):
    data_prep = DataPreparation(crypto_symb, start_date, end_date)
    data_prep.getData()