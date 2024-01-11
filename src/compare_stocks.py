import streamlit as st
from settings import DATASET_DIR
import requests, math, os
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from requests_html import HTMLSession
from streamlit_pagination import pagination_component
from pycoingecko import CoinGeckoAPI


class StockCompare:
    
    def __init__(self):
        self.file_path = DATASET_DIR + '/' + 'processed_data/crypto_data.csv'
        self.cg = CoinGeckoAPI()

    def visualizeData(self):
        df = pd.read_csv(self.file_path)
        # Handle NaN values
        df.fillna(0, inplace=True) 
        
        # Columns to exclude
        columns_to_exclude = ['id', 'symbol', 'image', 'price_change_percentage_24h',
                            'market_cap_rank', 'market_cap_change_24h', 'market_cap_change_percentage_24h',
                            'ath_change_percentage', 'atl_change_percentage', 'roi',
                            'price_change_percentage_1h_in_currency',
                            'price_change_percentage_24h_in_currency',
                            'price_change_percentage_7d_in_currency']

        # Exclude specified columns
        df = df.drop(columns=columns_to_exclude, errors='ignore')
        
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
        
        page_number = max(1, min(page_number, total_pages))

        # Calculate start and end indices for pagination
        start_index = (page_number - 1) * items_per_page
        end_index = min(start_index + items_per_page, len(df))
        
        # Display dataframe with pagination
        styled_df = df.iloc[start_index:end_index].style
        
        # Highlight max values in 'total_volume' column
        styled_df = styled_df.highlight_max(axis=0, subset=['current_price', 'market_cap', 'price_change_24h' ,'total_volume', 'high_24h', 'low_24h', 'max_supply', 'atl' ,'total_supply'])

       
        # Display dataframe with pagination
        styled_df = styled_df.set_table_styles(
            [{'selector': 'table', 
              'props': [('width', '800px'), ('height', '800px')]
              }]
        )
        st.write(styled_df)
        
        # Display "Page X of Y" indicator
        st.text(f"Page {page_number} of {total_pages}")
        
        st.subheader("Statistical summary")
        st.dataframe(df.describe())
        
        
    
    def currencyConversion(self, amount, from_currency, to_currency):
        try:
            if from_currency.lower() == 'XRP':
                from_currency = 'binance-peg-xrp'
                print(from_currency)
            if to_currency.lower() == 'XRP':
                to_currency = 'binance-peg-xrp'
            from_value = self.cg.get_price(ids=from_currency, vs_currencies='usd')[from_currency]['usd']
            to_value = self.cg.get_price(ids=to_currency, vs_currencies='usd')[to_currency]['usd']
            converted_amount = (amount * from_value) / to_value
            return converted_amount
        except KeyError as e:
            print(f"Error in currency conversion: {e}")
            return None
               
    def topPerformers(self):
        df = pd.read_csv(self.file_path).copy()
        sorted_data = df.sort_values(by='price_change_percentage_24h', ascending=False)
                        
        names = sorted_data['name']
        percent_change = sorted_data['price_change_percentage_24h'].astype(float)
        
        # Bar chart of percentage changes for top performers
        fig_bar = go.Figure(data=go.Bar(x=names, y=percent_change))
        fig_bar.update_layout(title='Top Cryptocurrency Performers Based on Percentage Change (Bar Chart)',
                            xaxis_title='Cryptocurrency', yaxis_title='% Change in 24h')

        # Scatter plot of percentage changes for top performers
        fig_scatter = go.Figure(data=go.Scatter(x=names, y=percent_change, mode='markers'))
        fig_scatter.update_layout(title='Top Cryptocurrency Performers Based on Percentage Change (Scatter Plot)',
                                xaxis_title='Cryptocurrency', yaxis_title='% Change in 24h')

        # Line chart of percentage changes for top performers
        fig_line = go.Figure(data=go.Scatter(x=names, y=percent_change, mode='lines+markers'))
        fig_line.update_layout(title='Top Cryptocurrency Performers Based on Percentage Change (Line Chart)',
                            xaxis_title='Cryptocurrency', yaxis_title='% Change in 24h')

       
        # Display charts using Streamlit
        st.plotly_chart(fig_bar)
        st.plotly_chart(fig_scatter)
        st.plotly_chart(fig_line)
    
    
    def pieChart(self):
        df = pd.read_csv(self.file_path).copy()

        # Convert 'Circulating Supply' to string
        # df['circulating_supply'] = df['circulating_supply'].astype(str)

        # Assuming 'Symbol' and 'Circulating Supply' are the relevant columns in your DataFrame
        symbols = df['symbol']
        # circulating_supply = df['circulating_supply']
        volume = df['total_volume']

        # Create a Pie Chart
        fig_pie = go.Figure(data=[go.Pie(labels=symbols, values=volume, hole=0.4)])

        # Customize the layout
        fig_pie.update_traces(textposition='inside', textinfo='percent+label')
        fig_pie.update_layout(title='Total Volume Distribution')

        # Display the Pie Chart using Streamlit
        st.plotly_chart(fig_pie)
    
    
    def heatmapChart(self):
        df = pd.read_csv(self.file_path).copy()

        # Assuming you have multiple numerical columns for correlation analysis
        numerical_columns = df.select_dtypes(include='number')

        # Create a correlation matrix
        correlation_matrix = numerical_columns.corr()

        # Create a Heatmap
        fig_heatmap = go.Figure(go.Heatmap(
            z=correlation_matrix.values,
            x=numerical_columns.columns,
            y=numerical_columns.columns,
            colorscale='Viridis',  # Choose a color scale
        ))

        # Customize the layout
        fig_heatmap.update_layout(title='Correlation Heatmap',
                                  height=600,  # Adjust the height as needed
                                  width=800,
                                  xaxis=dict(title='Variables'),
                                  yaxis=dict(title='Variables'))

        # Display the Heatmap using Streamlit
        st.plotly_chart(fig_heatmap)


        
        
def getStockData(file_path):
    url = f'https://api.coingecko.com/api/v3/coins/markets'
    params = {
        'vs_currency': 'usd',  # You can change this to another currency if needed
        'order': 'market_cap_desc',
        'per_page': 250,
        'page': 1,
        'sparkline': False,
        'price_change_percentage': '1h,24h,7d',  # Additional data (1-hour, 24-hour, 7-day price change percentage)
        'market_data': 'true',  # Include additional market data
    }
    
    try:
        # Make the API request
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise an exception for HTTP errors

        # Parse the JSON response
        data = response.json()

        # Extract relevant information
        top_cryptos = []
        for crypto in data:
            crypto_info = {
                'symbol': crypto['symbol'],
                'name': crypto['name'],
                'current_price': crypto['current_price'],
                'market_cap': crypto['market_cap'],
                'volume': crypto['total_volume'],
                'high_24h': crypto['high_24h'],
                'low_24h': crypto['low_24h'],
                'price_change_percentage_1h': crypto['price_change_percentage_1h_in_currency'],
                'price_change_percentage_24h': crypto['price_change_percentage_24h_in_currency'],
                'price_change_percentage_7d': crypto['price_change_percentage_7d_in_currency'],
                'close_24h': crypto['last_updated'],  # Assuming 'last_updated' is the close value
            }
            top_cryptos.append(crypto_info)

        df = pd.DataFrame(data)
        df.to_csv(file_path+'crypto_data.csv', index=False)
        currencies = df['symbol'].unique()
        return currencies

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from CoinGecko API: {e}")
        return None
    


def main():
    st.markdown("<h1>Exploring <span style='color: #b97010;'>Cryptocurrency</span> 💲 Data</h1>", unsafe_allow_html=True)
    file_path = DATASET_DIR + '/' + 'processed_data/'
    
    # Check if 'crypto_data.csv' file exists
    if not os.path.isfile(file_path + 'crypto_data.csv'):
        currency_list = getStockData(file_path)
    else:
        df = pd.read_csv(file_path + 'crypto_data.csv')
        currency_list = df['name'].unique().tolist()
    
    
    stkcmp = StockCompare()  
    
    st.sidebar.header("Select to Analyse Data")
    show_data = st.sidebar.checkbox('View data')
    show_pieChart = st.sidebar.checkbox('Show pie chart distribution')
    show_topPerformers = st.sidebar.checkbox('View top performers')
    show_heat_map = st.sidebar.checkbox('View heatmap Chart')
    show_calculator = st.sidebar.checkbox('Convert cryptocurrency')
    
    
    if show_data:
        stkcmp.visualizeData()
    
    if show_pieChart:
        stkcmp.pieChart()
    
    if show_topPerformers:
        st.markdown("<h3><span style='color: green;'>Top</span> performing Stocks 💲</h3>", unsafe_allow_html=True)
        stkcmp.topPerformers()

    if show_heat_map:
        stkcmp.heatmapChart()
    
    if show_calculator:
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