import streamlit as st
from settings import DATASET_DIR
import requests, math, os
import pandas as pd
import numpy as np
from requests_html import HTMLSession
from streamlit_pagination import pagination_component
from pycoingecko import CoinGeckoAPI


class StockCompare:
    
    def __init__(self):
        self.file_path = DATASET_DIR + '/' + 'processed_data/crypto_data.csv'
        self.cg = CoinGeckoAPI()
        # self.amount = amount
        # self.frm_curr = from_currency
        # self.to_curr = to_currency

    def visualizeData(self):
        df = pd.read_csv(self.file_path)
        # print(df)
        df = df.drop(columns="Name")
        style = """
        <style>
        th {
            white-space: nowrap;
            text-overflow: ellipsis;
            overflow: hidden;
            max-width: 300px; /* Adjust the maximum width */
            vertical-align: top;
        }
        </style>
        """
        st.markdown(style, unsafe_allow_html=True)
        
        # st.dataframe(df.style.highlight_max(axis=0), width=400, height=700)
        # Items per page
        items_per_page = 10

        # Sidebar - Page selection
        page_number = st.number_input("Select a page number", min_value=1, value=1)
        
        # Calculate total number of pages
        total_pages = math.ceil(len(df) / items_per_page)

        # Calculate start and end indices for pagination
        start_index = (page_number - 1) * items_per_page
        end_index = start_index + items_per_page

       
        # Display dataframe with pagination
        styled_df = df.iloc[start_index:end_index].style.highlight_max(axis=0).set_table_styles(
            [{'selector': 'table', 
              'props': [('width', '800px'), ('height', '800px')]
              }]
        )
        st.write(styled_df)
        
        # Display "Page X of Y" indicator
        st.text(f"Page {page_number} of {total_pages}")
        
        st.dataframe(df.describe())
        
        # statistical summaries
        
        # st.dataframe(df.describe())
        
        #top performers
        
    
    def currencyConversion(self, amount, from_currency, to_currency):
        from_value = self.cg.get_price(ids=from_currency, vs_currencies='usd')[from_currency]['usd']
        to_value = self.cg.get_price(ids=to_currency, vs_currencies='usd')[to_currency]['usd']
        converted_amount = (amount * from_value) / to_value
        return converted_amount
               
    


def getStockData(file_path):
    session = HTMLSession()
    num_currencies = 250
    resp = session.get(f"https://finance.yahoo.com/crypto?offset=0&count={num_currencies}")
    tables = pd.read_html(resp.html.raw_html)
    crypto = tables[0].copy()
    
    # Remove unwanted columns
    columns_to_drop = ["52 Week Range", "Day Chart"]
    crypto.drop(columns=columns_to_drop, inplace=True)
    
    # Save to a CSV file
    crypto.to_csv(file_path+'crypto_data.csv', index=False)  # Saves the DataFrame to a CSV file
    
    # Get unique cryptocurrency symbols from the dataset
    df = pd.read_csv(file_path + 'crypto_data.csv')
    currencies = df['Name'].unique()
    return currencies


def main():
    st.markdown("<h1>Exploring <span style='color: #b97010;'>Cryptocurrency</span> 💲 Data</h1>", unsafe_allow_html=True)
    file_path = DATASET_DIR + '/' + 'processed_data/'
    # Check if 'crypto_data.csv' file exists
    if not os.path.isfile(file_path + 'crypto_data.csv'):
        currency_list = getStockData(file_path)
    else:
        df = pd.read_csv(file_path + 'crypto_data.csv')
        currency_list = df['Name'].unique().tolist()
    
    # print(currency_list)
    
    stkcmp = StockCompare()    
    stkcmp.visualizeData()
    
    st.markdown("<h3><span style='color: #b97010;'>Cryptocurrency</span> 💲 Conversion</h3>", unsafe_allow_html=True)

    with st.form(key='conversion_form'):
        # A selectbox for symbol selection in the sidebar inside the form
        amount = st.number_input("Enter amount")
        from_currency = st.selectbox("From currency", currency_list)
        
        # Update currency_list for to_currency by removing from_currency
        to_currency_options = [currency for currency in currency_list if currency != from_currency]
        to_currency = st.selectbox("To currency", to_currency_options)
        
        # Add a form submit button
        submit_button = st.form_submit_button(label='Convert')
        if submit_button:
            result = stkcmp.currencyConversion(amount, from_currency.replace("USD", "").strip().lower(), to_currency.replace("USD", "").strip().lower())
            if result is not None:
                st.write(f"Equivalent amount: {amount} {from_currency.upper()} = {result:.2f} {to_currency.upper()}")
            else:
                st.warning("Invalid currency")


if __name__ == '__main__':
    main()