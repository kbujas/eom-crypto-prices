import csv
from datetime import datetime
from typing import Dict

from coingecko_api import get_eom_prices_coingecko
from coinmarketcap_api import get_prices_by_symbol_coin_market_cap
from data_prepping import get_coingecko_timestamps, get_ids_and_names, get_first_hour_current_month, get_symbols_list


end_of_month_timestamp = get_first_hour_current_month()

eom_date = datetime.fromtimestamp(end_of_month_timestamp)

coingecko_timestamps = get_coingecko_timestamps(
    init_timestamp=end_of_month_timestamp)    # Used for CoinGecko

symbols_list = get_symbols_list()

symbol_ids, symbol_names = get_ids_and_names(symbols_list=symbols_list)

def get_symbol_prices() -> Dict[str, float]:

    print('Gathering end-of-month prices from CoinMarketCap.com ...')

    prices_by_symbol, unpriced_symbols = \
        get_prices_by_symbol_coin_market_cap(timestamp=end_of_month_timestamp,
                                             ids=symbol_ids)
    
        
    if unpriced_symbols is not None:
        unpriced_symbol_names = {symbol: symbol_names[symbol] for symbol in unpriced_symbols if symbol in symbol_names.keys()}
        print('Gathering end-of-month prices from CoinGecko.com ...')
        prices_by_symbol = get_eom_prices_coingecko(symbol_names=unpriced_symbol_names,
                                                    timestamps=coingecko_timestamps,
                                                    symbol_prices=prices_by_symbol)

            
    return prices_by_symbol

def create_csv():

    # Specify the file name
    month, year = eom_date.month, eom_date.year
    filename = f"prices_end-of-month_{month-1}-{year}.csv"

    symbol_prices = get_symbol_prices()

    print(f'Writing {filename}')

    # Write dictionary to CSV file
    with open(filename, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['Symbol', 'Price (GBP)', 'Source'])
        writer.writeheader()
        # Assuming the dictionary lists are of equal length
        for key, value in symbol_prices.items():
            writer.writerow({'Symbol':key, 'Price (GBP)': value[0], 'Source': value[1]})

    print(f'Finished writing {filename}')

if __name__ == '__main__':
    create_csv()