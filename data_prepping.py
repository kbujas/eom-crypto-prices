from datetime import datetime, timedelta
from typing import Dict, List, Tuple
import requests


ids_url = 'https://s3.coinmarketcap.com/generated/core/crypto/cryptos.json'  
names_url = 'https://api.coingecko.com/api/v3/coins/list'

def get_first_hour_current_month() -> int:
    # Get the current date and time
    now = datetime.now()

    # Determine the first day of the current month
    first_day_current_month = now.replace(day=1, hour=0, minute=0, second=0)

    return first_day_current_month.timestamp()

def get_last_hour_timestamp(year: int, month: int) -> int:
    # Function to determine if a year is a leap year
    def is_leap_year(year: int) -> bool:
        return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)
    
    # Dictionary to hold the number of days in each month
    days_in_month = {
        1: 31,
        2: 29 if is_leap_year(year) else 28,
        3: 31,
        4: 30,
        5: 31,
        6: 30,
        7: 31,
        8: 31,
        9: 30,
        10: 31,
        11: 30,
        12: 31
    }
    
    # Get the last day of the month
    last_day = days_in_month[month]
    
    # Create a datetime object for the last hour of the last day of the month
    last_hour = datetime(year, month, last_day, 23, 59, 59)
    
    # Return the timestamp
    return int(last_hour.timestamp())


def get_symbols_list(txt_file_path: str='assets.txt'
                     ) -> List[str]:

    # Open the file in read mode
    with open(txt_file_path, 'r') as file:
        # Read the contents of the file into a string
        symbols = file.read().split()

    return symbols

def get_ids_and_names(symbols_list: list) -> Tuple[dict, dict]:
    id_response = requests.get(ids_url)
    names_response = requests.get(names_url)
    
    id_dict = dict()
    names_dict = dict()

    # Check if the request was successful
    if id_response.status_code == 200:
        id_data_list = id_response.json()['values']
        for element in id_data_list:
            id_num, symbol = element[0], element[2]
            if symbol in symbols_list:
                if id_dict.get(symbol) is None:
                    id_dict[symbol] = id_num
    else:
        print(f"Request failed with status code {id_response.status_code}")
    
        # Check if the request was successful
    if names_response.status_code == 200:
        names_data_list = names_response.json()
        for coin in names_data_list:
            symbol = coin['symbol'].upper()
            if symbol in symbols_list:
                names_dict[symbol] = coin['id']

    else:
        print(f"Request failed with status code {names_response.status_code}")

        
    return id_dict, names_dict



def find_eom_value(d: Dict[str, dict], 
                   timestamp: int
                   ) -> dict:
    # Extract the keys from the dictionary
    keys = list(d.keys())

    # Filter the keys to get those that are smaller than x
    filtered_keys = [key for key in keys if int(key) <= timestamp]

    # Find the maximum key from the filtered keys
    if filtered_keys:
        max_key = max(filtered_keys)
        return d[max_key]
    else:
        print(f"No keys are smaller than {timestamp}")

def get_coingecko_timestamps(init_timestamp):

    dt_last_hour = datetime.fromtimestamp(init_timestamp)
    to_timestamp = (dt_last_hour + timedelta(hours=1)).timestamp()

    return (init_timestamp, to_timestamp)
