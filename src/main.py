import streamlit as st
import datetime
from symbol_extract import ExtractSymbol
from data_preparation import DataPreparation

st.title("Visualize and Explore Cryptocurrencies Data")

# Binance API endpoint for historical kline/candlestick data
url = 'https://api.binance.com/api/v3/klines'

# A selectbox to the sidebar for symbol selection
extractor = ExtractSymbol(url='https://api.binance.com/api/v3/ticker/24hr')
symbols_list = extractor.getSymbols()

# Create a form context
with st.sidebar.form(key='my_form'):
    # A selectbox for symbol selection in the sidebar inside the form
    crypto_symb = st.selectbox(
        'Select a crypto symbol',
        symbols_list[:100]
    )

    # start and end date for data
    today = datetime.datetime.now().date()
    start_year = datetime.date(2000, 1, 1)
    end_year = today
    
    date_range = st.date_input(
        "Select date range for data",
        (start_year, end_year),
        start_year,
        today,
        format="YYYY-MM-DD",
    )
    
    print(date_range)
    # start_date = int(datetime.datetime(start_year.year, start_year.month, start_year.day).timestamp())
    # end_date = int(datetime.datetime(end_year.year, end_year.month, end_year.day).timestamp())
    start_date = int(start_year.replace(hour=0, minute=0, second=0).timestamp()) * 1000
    end_date = int(end_year.replace(hour=0, minute=0, second=0).timestamp()) * 1000
    
    # Add a form submit button
    submit_button = st.form_submit_button(label='Submit')
    
    # preparation of raw data
    if submit_button:
        if crypto_symb is not None:
            data_prep = DataPreparation(crypto_symb, start_date, end_date)
            data_prep.getData()
        else:
            st.warning("Please select a crypto symbol before submitting")
