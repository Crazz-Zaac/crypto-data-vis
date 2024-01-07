import streamlit as st
import datetime
from symbol_extract import ExtractSymbol
from data_preparation import DataPreparation
from streamlit_date_picker import date_range_picker, PickerType, Unit, date_picker
from data_cleaning import DataClean

st.title("Visualize and Explore Cryptocurrencies Data")

# Binance API endpoint for historical kline/candlestick data
url = 'https://api.binance.com/api/v3/klines'

def marketCap(self):
    # Market Cap visualization of 250 Crypto currencies
    import plotly.express as px
    stock_data = pd.read_csv(self.clean_dataset_path + 'crypto_data.csv')
    fig = px.bar(stock_data, x='Name', y='Market Cap', title='Market Cap Comparison')
    fig.update_layout(height=600)
    st.plotly_chart(fig, use_container_width=True)

# A selectbox to the sidebar for symbol selection
extractor = ExtractSymbol(url='https://api.binance.com/api/v3/ticker/24hr')
symbols_list = extractor.getSymbols()

# Create a form context
@st.cache_data
with st.sidebar.form(key='my_form'):
    # A selectbox for symbol selection in the sidebar inside the form
    crypto_symb = st.selectbox(
        'Select a crypto symbol',
        symbols_list[:99]
    )

    # Use date_picker to create a date picker
    st.subheader('Start Date Picker')
    start_date_string = date_picker(picker_type=PickerType.time.string_value, value=0, unit=Unit.days.string_value,
                            key='start_date_picker')

    if start_date_string is None:
        today = datetime.datetime.now()
        start_date_string = (today - datetime.timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S')
    
    st.subheader('End Date Picker')
    end_date_string = date_picker(picker_type=PickerType.time.string_value, value=0, unit=Unit.days.string_value,
                            key='end_date_picker')

    if end_date_string is None:
        today = datetime.datetime.now()
        end_date_string = today.strftime('%Y-%m-%d %H:%M:%S')
    
    print(start_date_string, end_date_string)
    
    date_obj1 = datetime.datetime.strptime(start_date_string, '%Y-%m-%d %H:%M:%S')
    date_obj2 = datetime.datetime.strptime(end_date_string, '%Y-%m-%d %H:%M:%S')
    
    start_date = datetime.datetime(date_obj1.year, date_obj1.month, date_obj1.day, date_obj1.hour, date_obj1.minute, date_obj1.second)
    end_date = datetime.datetime(date_obj2.year, date_obj2.month, date_obj2.day, date_obj2.hour, date_obj2.minute, date_obj2.second)
    
    start_time = int(start_date.timestamp()) * 1000  # Multiply by 1000 to convert to milliseconds
    end_time = int(end_date.timestamp()) * 1000  # Multiply by 1000 to convert to milliseconds
    
    print(start_time, end_time)
    
    # Add a form submit button
    submit_button = st.form_submit_button(label='Prepare Data')
    
    # Preparation of raw data
    if submit_button:
        if crypto_symb is not None:
            data_prep = DataPreparation(crypto_symb, start_time, end_time)
            data_prep.getData()
        else:
            st.warning("Please select a crypto symbol before submitting")


# if st.sidebar.button("Clean Data"):
st.sidebar.header("Visualize Data")
option = st.sidebar.selectbox('Choose an option',
                              ('','View Data', 'View Candlestick', 'Compare multiple stocks'))
if option == 'View Candlestick':
    
