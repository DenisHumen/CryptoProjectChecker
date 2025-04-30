import requests
import json
from datetime import datetime
import csv
from colorama import Fore, Style
from concurrent.futures import ThreadPoolExecutor, as_completed, TimeoutError

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
    bar_length = 40  # Length of the progress bar
    total_wallets = len(wallets)
    completed_wallets = 0

    def process_wallet_task(wallet_address, proxy):
        try:
            result = example_checker(wallet_address, proxy)
            return result, True  # Return result and success status
        except Exception as e:
            log_error(f"Error processing wallet {wallet_address}: {str(e)}")
            return wallet_address, False  # Return wallet address and failure status

    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        future_to_wallet = {executor.submit(process_wallet_task, wallet, proxy): wallet for wallet, proxy in zip(wallets, proxies)}
        for future in as_completed(future_to_wallet):
            wallet = future_to_wallet[future]
            try:
                result, success = future.result(timeout=10)  # Ensure thread doesn't hang for more than 10 seconds
                if success:
                    results.append(result)
                    print(Fore.GREEN + f" | 🟢 Wallet: {wallet}" + Style.RESET_ALL, end="\r")
                else:
                    log_error(f"Failed to process wallet: {wallet}")
                    print(Fore.RED + f" | ❌ Wallet (check 'results/logs/log)': {wallet}" + Style.RESET_ALL, end="\r")
            except TimeoutError:
                log_error(f"Timeout error for wallet {wallet}")
                print(Fore.RED + f" | ❌ Timeout for wallet (check 'results/logs/log)': {wallet}" + Style.RESET_ALL, end="\r")
            except Exception as e:
                log_error(f"Unhandled exception for wallet {wallet}: {str(e)}")
                print(Fore.RED + f" | ❌ Exception for wallet (check 'results/logs/log)': {wallet}" + Style.RESET_ALL, end="\r")
            finally:
                completed_wallets += 1
                progress = int((completed_wallets / total_wallets) * bar_length)
                bar = "█" * progress + "░" * (bar_length - progress)
                print(f"\r[{bar}] {completed_wallets}/{total_wallets}", end="", flush=True)

    print()  # Move to the next line after the progress bar is complete
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
