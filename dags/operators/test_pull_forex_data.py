def test_pull_forex_data(formatter, api_key, save_path, ti):
    # # mimics replacement of file path when returned from pull_forex_data task
    # # relative file path
    # new_file_path = "./include/data/usd_php_forex_4hour.csv"

    # absolute file path
    new_file_path = "/usr/local/airflow/include/data/usd_php_forex_4hour.csv"
    ti.xcom_push(key="new_file_path", value=new_file_path)

    print()
    print(f"api_key: {api_key}")
    print(f"save_path: {save_path}")