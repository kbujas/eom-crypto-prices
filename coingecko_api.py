from typing import Dict, Tuple
import requests
from datetime import datetime
import time

from data_prepping import get_coingecko_timestamps, get_first_hour_current_month

# Define the base URL for the CoinGecko API
base_url = 'https://api.coingecko.com/api/v3'

# Define the endpoint for historical market data
endpoint = '/coins/{id}/market_chart/range'

# Define the parameters for the API request
coin_id = 'bitcoin'  # Cryptocurrency ID
vs_currency = 'gbp'  # Fiat currency
start_date = '2024-05-31'  # Start date in YYYY-MM-DD format
end_date = '2024-06-01'    # End date in YYYY-MM-DD format

# Convert date to UNIX timestamps
start_timestamp = int(datetime.strptime(start_date, '%Y-%m-%d').timestamp())
end_timestamp = int(datetime.strptime(end_date, '%Y-%m-%d').timestamp())

# print(datetime.fromtimestamp(end_timestamp))

def get_symbol_eom_price_coingecko(timestamps: Tuple[int, int],
                     coin_id: str,
                     vs_currency: str='gbp'
                     ) -> float:
 
    start_timestamp, end_timestamp = timestamps

    parameters = {
        'vs_currency': vs_currency,
        'from': start_timestamp,
        'to': end_timestamp
    }

    # Construct the full API URL with the endpoint and parameters
    api_url = f"{base_url}/coins/{coin_id}/market_chart/range"

    # Make the GET request to the CoinGecko API
    response = requests.get(api_url, params=parameters)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()

        try:

            price = data.get('prices')[0][1]
            return price
        
        except IndexError:
            print(data, coin_id)
    else:
        print(f"Error - {coin_id}: {response.status_code}, {response.text}")
        return 'None'
    
def get_eom_prices_coingecko(symbol_names: dict,
                             symbol_prices: Dict[str, float],
                             timestamps: Tuple[int, int]
                             ) -> Dict[str, float]:
    
    for symbol, name in symbol_names.items():
        price = get_symbol_eom_price_coingecko(timestamps=timestamps,
                                               coin_id=name)
        symbol_prices[symbol] = [price, 'Coingecko']
        time.sleep(15)   # Work around the rate limit


    return symbol_prices

