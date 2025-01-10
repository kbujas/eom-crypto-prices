import requests
from data_prepping import find_eom_value


def get_price_at_eom_coin_market_cap(id_num: int, 
                                     timestamp: int
                                     ) -> float:
    url = \
        f'https://api.coinmarketcap.com/data-api/v3/cryptocurrency/detail/chart?id={id_num}&range=1M&convertId=2791'
    prices_response = requests.get(url)

    if prices_response.status_code == 200:
        price_data = prices_response.json()
        if price_data['data'].get('points') is None:
            return None
        points_dict = price_data['data']['points']
        eom_price_data = find_eom_value(d=points_dict, timestamp=timestamp)
        price = eom_price_data['c'][0]
        
        return price

    else:
        print(f"Request failed with status code {prices_response.status_code}")

def get_prices_by_symbol_coin_market_cap(ids: dict,
                                         timestamp: int
                                         ) -> dict:

    price_by_symbol = dict()

    for symbol, id_num in ids.items():
        price = get_price_at_eom_coin_market_cap(id_num=id_num, timestamp=timestamp)
        if price is not None:
            price_by_symbol[symbol] = [price, 'CoinMarketCap']
    
    priced_symbols = set(list(price_by_symbol.keys()))
    unpriced_symbols = list(set(list(ids.keys())).difference(priced_symbols))
    

    if len(unpriced_symbols) != 0:
        return price_by_symbol, unpriced_symbols

    return price_by_symbol, None