import streamlit as st
from settings import DATASET_DIR
import requests, math
import pandas as pd
import numpy as np
from requests_html import HTMLSession
from streamlit_pagination import pagination_component



class StockCompare:
    
    def __init__(self, amount, from_currency, to_currency):
        self.file_path = DATASET_DIR + '/' + 'processed_data/crypto_data.csv'' 
        self.amount = amount
        self.frm_curr = from_currency
        self.to_curr = to_currency

    def visualizeData(self):
        df = pd.read_csv(self.file_path+'crypto_data.csv')
        # print(df)
        # df.drop(columns=["Name", "52 Week Range", "Day Chart"], inplace=True, axis=1)
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
        
        
        # statistical summaries
        
        # st.dataframe(df.describe())
        
        #top performers
        
    
    def currencyConversion(self):
        df = pd.read_csv(self.file_path)
        if from_currency not in df['Symbol'].values or to_currency not in df['Symbol'].values:
            return None  # Invalid currency
        
        from_value = df.loc[df['Symbol'] == from_currency, 'Price'].values[0]
        to_value = df.loc[df['Symbol'] == to_currency, 'Price'].values[0]

        converted_amount = (amount * to_value) / from_value
        return converted_amount
        
    


def getStockData(file_path):
    session = HTMLSession()
    num_currencies = 250
    resp = session.get(f"https://finance.yahoo.com/crypto?offset=0&count={num_currencies}")
    tables = pd.read_html(resp.html.raw_html)
    crypto = tables[0].copy()
    
    # Remove unwanted columns
    columns_to_drop = ["Name", "52 Week Range", "Day Chart", "Supply"]
    crypto.drop(columns=columns_to_drop, inplace=True)
    
    # Save to a CSV file
    crypto.to_csv(file_path+'crypto_data.csv', index=False)  # Saves the DataFrame to a CSV file
    
    # Get unique cryptocurrency symbols from the dataset
    df = pd.read_csv(stkcmp.file_path + 'crypto_data.csv')
    currencies = df['Symbol'].unique()
    return currencies


def main():
    file_path = DATASET_DIR + '/' + 'processed_data/'
    currency_list = getStockData(file_path)
    
    amount = st.number_input("Enter amount")
    from_currency = st.selectbox("From currency", currencies)
    
    
    
    
    stkcmp = StockCompare()
    stkcmp.getStockData()
    stkcmp.visualizeData()


if __name__ == '__main__':
    main()