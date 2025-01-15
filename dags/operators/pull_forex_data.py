import pandas as pd
import requests
from requests import HTTPError, ConnectionError, JSONDecodeError, ConnectTimeout, Timeout
import time 
import re


def pull_forex_data(start_date: str='january 1 2024',
    end_date: str='january 1 2025',
    forex_ticker: str="C:USDPHP",
    multiplier: int=4,
    timespan: str='hour',
    formatter=None,
    api_key=None) -> None:
    
    start_date_reformed = start_date if formatter == None else formatter(start_date)
    end_date_reformed = end_date if formatter == None else formatter(end_date)

    params = {
        "adjusted": True,
        "sort": "asc",
        # "limit": 1,
    }

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    url = f"https://api.polygon.io/v2/aggs/ticker/{forex_ticker}/range/{multiplier}/{timespan}/{start_date_reformed}/{end_date_reformed}"
    
    data_batches = []
    interval = 5
    start = 0

    try:
        while True:
            response = requests.get(url, params=params, headers=headers)
            
            if response.status_code == 200:
                data_batch = response.json()
                print(data_batch)
                if not "next_url" in data_batch:
                    break

                df = pd.DataFrame(data_batch['results'])
                data_batches.append(df)
                url = data_batch['next_url']

                # sleep for 1 minute to avoid rate limiting
                if (start + 1) % interval == 0:
                    time.sleep(60)

                # increment after 60 seconds
                start += 1
            
            elif response.status_code == 401:
                continue
            
    except HTTPError as e:
        print(f'{e} has occured.')

    except (ConnectTimeout, Timeout) as e:
        print(f'{e} has occured.')

    except JSONDecodeError as e:
        print(f'error decoding json from response has occured.')

    # combine batches
    forex_data = pd.concat(data_batches, ignore_index=True, axis=0)

    # create name for dataframe
    ticker_name = re.sub(r"C:", "", forex_ticker)
    str_len = len(ticker_name)
    chunk_size = str_len // 2

    # will return usd_php
    ticker_name = "_".join([ticker_name[i:i + chunk_size].lower() for i in range(0, str_len, chunk_size)])
    
    # save dataframe to .csv
    forex_data.to_csv(f'./data/{ticker_name}_forex_{multiplier}{timespan}.csv')