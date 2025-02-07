import pandas as pd
import requests
from requests import HTTPError, ConnectionError, JSONDecodeError, ConnectTimeout, Timeout
import time 
import re
import os


def pull_forex_data(start_date,
    end_date,
    forex_ticker,
    multiplier,
    timespan,
    formatter,
    save_path,
    ti) -> None:
    """
    collects forex data from the Polygon API and stores the values in a dataframe
    to be uploaded in an S3 bucket
    """

    # get api key
    api_key = ti.xcom_pull(key="api_key", task_ids="get_env_vars")

    # reformat date
    start_date_reformed = start_date if formatter == None else formatter(start_date)
    end_date_reformed = end_date if formatter == None else formatter(end_date)

    # default parameters
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
    
    # initialize data batches where dataframes would be saved
    data_batches = []
    interval = 5
    start = 0

    print(url)
    print(headers)

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

    # # combine batches
    forex_data = pd.concat(data_batches, ignore_index=True, axis=0)
    # forex_data = pd.concat([pd.DataFrame(), pd.DataFrame()], ignore_index=True, axis=0)

    # create name for dataframe
    ticker_name = re.sub(r"C:", "", forex_ticker)
    str_len = len(ticker_name)
    chunk_size = str_len // 2

    # will return usd_php
    ticker_name = "_".join([ticker_name[i:i + chunk_size].lower() for i in range(0, str_len, chunk_size)])

    # save dataframe to .csv. Note that save path is '/usr/local/airflow/include/data'
    # file path of saved data would be '/usr/local/airflow/include/data/usd_php_forex_4hour.csv'
    file_path = os.path.join(save_path, f"{ticker_name}_forex_{multiplier}{timespan}.csv")
    forex_data.to_csv(file_path)

    # allow task to return file path of the saved .csv
    return file_path