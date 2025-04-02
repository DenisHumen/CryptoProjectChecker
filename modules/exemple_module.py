import requests
import json
import os
import random
import threading
from tqdm import tqdm
import time
from datetime import datetime
import csv
from colorama import Fore, Style

log_file_path = 'results/logs/log'

def log_error(message):
    with open(log_file_path, 'a') as log_file:
        log_file.write(message + '\n')

def parse_json_response(response):
    try:
        data = json.loads(response)

        example_field_1 = data['exampleField1']
        example_field_2 = data['exampleField2']
        nested_field = data['nestedField']['subField']
        timestamp = datetime.utcfromtimestamp(data['timestamp']).strftime('%Y-%m-%d %H:%M:%S')
        return {
            'example_field_1': example_field_1,
            'example_field_2': example_field_2,
            'nested_field': nested_field,
            'timestamp': timestamp
        }
    except (KeyError, ValueError, TypeError) as e:
        log_error(f'Error parsing response: {str(e)}')
        return {
            'example_field_1': '',
            'example_field_2': '',
            'nested_field': '',
            'timestamp': ''
        }

def example_checker(wallet_address, proxy):
    try:
        url = f'https://example.com/api/wallets/{wallet_address}'  
        params = {"example_param": "value"} 
        headers = {
            "accept": "application/json",
            "content-type": "application/json"
        }

        response = requests.get(url, params=params, headers=headers, proxies={"http": proxy, "https": proxy})
        
        if response.status_code != 200:
            log_error(f'HTTP error: {response.status_code} - {response.text}')
            raise ValueError(f'HTTP error: {response.status_code}')
        
        if not response.content:
            log_error(f'Empty response content - {response.text}')
            raise ValueError('Empty response content')
        
        try:
            data = response.json()
            data['wallet_address'] = wallet_address
            parsed_data = parse_json_response(json.dumps(data)) 
            data.update(parsed_data)  
        except json.JSONDecodeError:
            data = {"wallet_address": wallet_address, "response": response.text}
        
        file_path = f"results/wallet_json_data/{wallet_address}.json"
        with open(file_path, 'w') as json_file:
            json.dump(data, json_file)
        
        return data
    
    except requests.exceptions.ProxyError as e:
        log_error(f'Proxy {proxy} error: ' + str(e))
        raise e
    except requests.exceptions.RequestException as e:
        log_error('Request error: ' + str(e))
        raise e
    except Exception as e:
        log_error('Error: ' + str(e))
        raise e

def process_wallets(wallets, proxies, num_threads, sleep_between_wallet):
    results = []
    threads = []
    lock = threading.Lock()  
    with tqdm(total=len(wallets)) as pbar:
        def worker(wallet_address, proxy):
            nonlocal results
            try:
                result = example_checker(wallet_address, proxy)
                if result is not None: 
                    with lock:
                        results.append(result)
            except Exception as e:
                log_error(f"Error processing wallet {wallet_address}: {str(e)}")
            finally:
                pbar.update(1)

        for wallet_address, proxy in zip(wallets, proxies):
            if len(threads) >= num_threads:
                for t in threads:
                    t.join()
                threads = []
            thread = threading.Thread(target=worker, args=(wallet_address, proxy))
            thread.start()
            threads.append(thread)
            time.sleep(random.uniform(*sleep_between_wallet))
        
        for t in threads:
            t.join()
    
    process_results_to_csv(results)

    wallets_with_data = len([result for result in results if result is not None])
    wallets_without_data = len(wallets) - wallets_with_data

    print(Fore.GREEN + f"Wallets with data: {wallets_with_data}" + Style.RESET_ALL)
    print(Fore.RED + f"Wallets without data: {wallets_without_data}" + Style.RESET_ALL)

    return results

def process_results_to_csv(results):
    csv_file_path = 'results/result.csv'
    fieldnames = [
        'wallet_address', 'example_field_1', 'example_field_2',
        'nested_field', 'timestamp'
    ]

    with open(csv_file_path, mode='w', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

        for result in results:
            if result is not None:  
                writer.writerow({
                    'wallet_address': result.get('wallet_address', ''),
                    'example_field_1': result.get('example_field_1', ''),
                    'example_field_2': result.get('example_field_2', ''),
                    'nested_field': result.get('nested_field', ''),
                    'timestamp': result.get('timestamp', '')
                })
