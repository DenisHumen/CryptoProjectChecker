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

# Fixed pyload
pyload1 = {
    "jsonrpc": "2.0",
    "id": 1,
    "method": "get_account",
    "params": "0x"
}

def log_error(message):
    with open(log_file_path, 'a') as log_file:
        log_file.write(message + '\n')

def parse_json_response(response):
    try:
        data = json.loads(response)
        top_percent = data['walletPerformance']['topPercent']
        transaction_count = data['widget']['data']['stats'][0]['value']
        interacted_contracts = data['widget']['data']['stats'][1]['value']
        contracts_created = data['widget']['data']['stats'][2]['value']
        wallet_balance = data['cardsList'][0]['data']['stats'][0]['value']
        active_days = data['cardsList'][1]['data']['activeDays']['value']
        active_weeks = data['cardsList'][1]['data']['activeWeeks']['value']
        active_months = data['cardsList'][1]['data']['activeMonths']['value']
        last_updated = datetime.utcfromtimestamp(data['lastUpdated']).strftime('%Y-%m-%d %H:%M:%S')
        return {
            'top_percent': top_percent,
            'transaction_count': transaction_count,
            'interacted_contracts': interacted_contracts,
            'contracts_created': contracts_created,
            'wallet_balance': wallet_balance,
            'active_days': active_days,
            'active_weeks': active_weeks,
            'active_months': active_months,
            'last_updated': last_updated
        }
    except (KeyError, ValueError, TypeError) as e:
        log_error(f'Error parsing response: {str(e)}')
        return {
            'top_percent': '',
            'transaction_count': '',
            'interacted_contracts': '',
            'contracts_created': '',
            'wallet_balance': '',
            'active_days': '',
            'active_weeks': '',
            'active_months': '',
            'last_updated': ''
        }

def megaeth_checker(wallet_address, proxy, pyload=pyload1):
    if pyload is not None:
        try:
            url = f'https://layerhub.xyz/be-api/wallets/megaeth_testnet/{wallet_address}'
            params = {"_rsc": "1qmdk"}
            headers = {
                "accept": "*/*",
                "accept-language": "ru,en-US;q=0.9,en;q=0.8",
                "content-type": "application/json",
                "sec-ch-ua": "\"Not A(Brand\";v=\"8\", \"Chromium\";v=\"132\", \"Google Chrome\";v=\"132\"",
                "sec-ch-ua-mobile": "?0",
                "sec-ch-ua-platform": "\"Linux\"",
                "sec-fetch-dest": "empty",
                "sec-fetch-mode": "cors",
                "sec-fetch-site": "same-origin"
            }

            response = requests.get(url, params=params, headers=headers, proxies={"http": proxy, "https": proxy})
            
            if response.status_code == 404:
                error_message = response.json().get("message", "")
                if error_message == "Wallet is not found for chain_id: megaeth_testnet":
                    log_error(f"Wallet {wallet_address} |MegaETH| not found, skipping...")
                    return None  # Skip this wallet
                else:
                    log_error(f'HTTP error: {response.status_code} - {response.text}')
                    raise ValueError(f'HTTP error: {response.status_code}')
            
            if response.status_code != 200:
                log_error(f'HTTP error: {response.status_code} - {response.text}')
                raise ValueError(f'HTTP error: {response.status_code}')
            
            if not response.content:
                log_error(f'Empty response content - {response.text}')
                raise ValueError('Empty response content')
            
            try:
                data = response.json()
                data['wallet_address'] = wallet_address
                parsed_data = parse_json_response(json.dumps(data))  # Parse the response
                data.update(parsed_data)  # Merge parsed data into the original data
            except json.JSONDecodeError:
                data = {"wallet_address": wallet_address, "response": response.text}
            
            # Save the result to a JSON file immediately
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

    else:
        log_error(f'Error: No pyload found {pyload}')

def process_wallet(wallet_address, proxy, reserv_proxies, results, sleep_between_replace_proxy, limit_replace_proxy):
    success = False
    attempts = 0
    while not success and attempts < limit_replace_proxy:
        try:
            result = megaeth_checker(wallet_address, proxy)
            if result is not None:  # Skip if result is None
                results.append(result)
            success = True
        except ValueError as e:
            log_error(str(e))
            time.sleep(random.uniform(*sleep_between_replace_proxy))
        except requests.exceptions.ProxyError as e:
            log_error(f'Proxy error with proxy {proxy}: ' + str(e))
            time.sleep(random.uniform(*sleep_between_replace_proxy))
            proxy = random.choice(reserv_proxies)
        except requests.exceptions.RequestException as e:
            log_error(f'Request error: ' + str(e))
            time.sleep(random.uniform(*sleep_between_replace_proxy))
        except json.JSONDecodeError as e:
            log_error(f'JSON decode error: ' + str(e))
            time.sleep(random.uniform(*sleep_between_replace_proxy))
        attempts += 1

def process_wallets(wallets, proxies, reserv_proxies, num_threads, sleep_between_wallet, sleep_between_replace_proxy, limit_replace_proxy):
    results = []
    threads = []
    lock = threading.Lock()  # To safely append results in multithreading
    with tqdm(total=len(wallets)) as pbar:
        def worker(wallet_address, proxy):
            nonlocal results
            try:
                result = megaeth_checker(wallet_address, proxy)
                if result is not None:  # Skip if result is None
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
    
    ensure_all_wallets_processed(wallets, proxies, reserv_proxies, results, sleep_between_replace_proxy, limit_replace_proxy)
    process_results_to_csv(results)

    # Count wallets with and without data
    wallets_with_data = len([result for result in results if result is not None])
    wallets_without_data = len(wallets) - wallets_with_data

    # Print results
    print(Fore.GREEN + f"Wallets with data: {wallets_with_data}" + Style.RESET_ALL)
    print(Fore.RED + f"Wallets without data: {wallets_without_data}" + Style.RESET_ALL)

    return results

def ensure_all_wallets_processed(wallets, proxies, reserv_proxies, results, sleep_between_replace_proxy, limit_replace_proxy):
    for wallet_address in wallets:
        file_path = f"results/wallet_json_data/{wallet_address}.json"
        if not os.path.exists(file_path):
            proxy = random.choice(reserv_proxies)
            process_wallet(wallet_address, proxy, reserv_proxies, results, sleep_between_replace_proxy, limit_replace_proxy)

def process_results_to_csv(results):
    csv_file_path = 'results/result.csv'
    fieldnames = [
        'wallet_address', 'top_percent', 'transaction_count', 'interacted_contracts',
        'contracts_created', 'wallet_balance', 'active_days', 'active_weeks',
        'active_months', 'last_updated'
    ]

    with open(csv_file_path, mode='w', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

        for result in results:
            if result is not None:  # Skip None results
                writer.writerow({
                    'wallet_address': result.get('wallet_address', ''),
                    'top_percent': result.get('top_percent', ''),
                    'transaction_count': result.get('transaction_count', ''),
                    'interacted_contracts': result.get('interacted_contracts', ''),
                    'contracts_created': result.get('contracts_created', ''),
                    'wallet_balance': result.get('wallet_balance', ''),
                    'active_days': result.get('active_days', ''),
                    'active_weeks': result.get('active_weeks', ''),
                    'active_months': result.get('active_months', ''),
                    'last_updated': result.get('last_updated', '')
                })

def json_to_csv(json_folder, csv_file_path):
    """
    Convert all JSON files in a folder to a single CSV file.
    """
    fieldnames = [
        'wallet_address', 'top_percent', 'transaction_count', 'interacted_contracts',
        'contracts_created', 'wallet_balance', 'active_days', 'active_weeks',
        'active_months', 'last_updated'
    ]

    results = []
    for filename in os.listdir(json_folder):
        if filename.endswith('.json'):
            file_path = os.path.join(json_folder, filename)
            with open(file_path, 'r') as json_file:
                try:
                    data = json.load(json_file)
                    results.append({
                        'wallet_address': data.get('wallet_address', ''),
                        'top_percent': data.get('top_percent', ''),
                        'transaction_count': data.get('transaction_count', ''),
                        'interacted_contracts': data.get('interacted_contracts', ''),
                        'contracts_created': data.get('contracts_created', ''),
                        'wallet_balance': data.get('wallet_balance', ''),
                        'active_days': data.get('active_days', ''),
                        'active_weeks': data.get('active_weeks', ''),
                        'active_months': data.get('active_months', ''),
                        'last_updated': data.get('last_updated', '')
                    })
                except json.JSONDecodeError as e:
                    log_error(f"Error decoding JSON file {filename}: {str(e)}")

    with open(csv_file_path, mode='w', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)

# Example usage:
# json_to_csv('results/wallet_json_data', 'results/result.csv')


