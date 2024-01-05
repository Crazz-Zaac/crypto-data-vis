class ExtractSymbol:
    def __init__(self, url):
        self.url = url

    def getSymbols(self):
        import requests
        response = requests.get(self.url)
        
        if response.status_code == 200:
            ticker_data = response.json()
            
            #sorting symbols by trading volume
            sorted_symbols = sorted(ticker_data, key=lambda x: float(x['quoteVolume']), reverse=True)
            symbols = [symbol['symbol'] for symbol in sorted_symbols]
            
            return tuple(symbols)

        else:
            raise Exception("Failed to fetch data.")
    
    