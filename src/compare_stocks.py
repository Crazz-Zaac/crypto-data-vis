import streamlit as st
from settings import DATASET_DIR
import requests, math
import pandas as pd
import numpy as np
from requests_html import HTMLSession
from streamlit_pagination import pagination_component



class StockCompare:
    
    def __init__(self, df):
        self.df = df 

    def visualizeData(self):
        
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
        
        # st.dataframe(self.df.style.highlight_max(axis=0), width=400, height=700)
        # Items per page
        items_per_page = 10

        # Sidebar - Page selection
        page_number = st.number_input("Select a page number", min_value=1, value=1)
        
        # Calculate total number of pages
        total_pages = math.ceil(len(self.df) / items_per_page)

        # Calculate start and end indices for pagination
        start_index = (page_number - 1) * items_per_page
        end_index = start_index + items_per_page

       
        # Display dataframe with pagination
        styled_df = self.df.iloc[start_index:end_index].style.highlight_max(axis=0).set_table_styles(
            [{'selector': 'table', 
              'props': [('width', '800px'), ('height', '800px')]
              }]
        )
        st.write(styled_df)
        
        # Display "Page X of Y" indicator
        st.text(f"Page {page_number} of {total_pages}")
        
        
        # statistical summaries
        
        # st.dataframe(self.df.describe())
        
        #top performers
        
    
    def currencyConversion(self):
        pass


@st.cache_data
def getStockData():
    file_path = DATASET_DIR + '/' + 'processed_data/' 
    session = HTMLSession()
    num_currencies = 250
    resp = session.get(f"https://finance.yahoo.com/crypto?offset=0&count={num_currencies}")
    tables = pd.read_html(resp.html.raw_html)
    crypto = tables[0].copy()
    # Save to a CSV file
    crypto.to_csv(file_path+'crypto_data.csv', index=False)  # Saves the DataFrame to a CSV file


def main():
    getStockData()
    df = pd.read_csv(DATASET_DIR + '/' + 'processed_data/'+'crypto_data.csv')
    df.drop(columns=["Name", "52 Week Range", "Day Chart"], inplace=True, axis=1)
    stkcmp = StockCompare(df)
    stkcmp.visualizeData()


if __name__ == '__main__':
    main()