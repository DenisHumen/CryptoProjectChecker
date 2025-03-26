import toml
import csv
import random
import threading
from tqdm import tqdm
from questionary import Choice, select
from colorama import Fore, Style
import os
import time
import requests
import json
from config.pyload_presset.random_pyload import random_pyload_presset
from modules.monad import monad_checker, process_json_to_csv
import modules.monad as monad

config = toml.load('config/general_config.toml')
num_threads = config.get('THRENDS', 10)
sleep_between_wallet = config.get('SLEEP_BEATWEEN_WALLET', [1, 3])
sleep_between_replace_proxy = config.get('SLEEP_BEATWEEN_REAPLECE_PROXY', [1, 3])
limit_replace_proxy = config.get('LIMIT_REPLACE_PROXY', 10)
log_file_path = 'results/logs/log'

def log_error(message):
    with open(log_file_path, 'a') as log_file:
        log_file.write(message + '\n')

def get_wallets_and_proxies():
    wallets = []
    proxies = []
    with open('data/wallet.csv', mode='r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        for row in reader:
            if len(row) >= 2:
                wallets.append(row[0])
                proxies.append(row[1])
    return wallets, proxies

def get_reserv_proxies():
    reserv_proxies = []
    with open('data/reserv_proxy.csv', mode='r') as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) > 0:
                reserv_proxies.append(row[0])
    return reserv_proxies

def process_wallets(wallets, proxies, reserv_proxies):
    results = []
    threads = []
    with tqdm(total=len(wallets)) as pbar:
        for wallet_address, proxy in zip(wallets, proxies):
            if len(threads) >= num_threads:
                for t in threads:
                    t.join()
                    pbar.update(1)
                threads = []
            thread = threading.Thread(target=process_wallet, args=(wallet_address, proxy, reserv_proxies, results))
            thread.start()
            threads.append(thread)
            time.sleep(random.uniform(*sleep_between_wallet))
        
        for t in threads:
            t.join()
            pbar.update(1)
    
    ensure_all_wallets_processed(wallets, proxies, reserv_proxies, results)
    return results

def process_wallet(wallet_address, proxy, reserv_proxies, results):
    pyload = random_pyload_presset()
    success = False
    attempts = 0
    while not success and attempts < limit_replace_proxy:
        try:
            result = monad_checker(wallet_address, proxy, pyload)
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

def ensure_all_wallets_processed(wallets, proxies, reserv_proxies, results):
    for wallet_address in wallets:
        file_path = f"results/wallet_json_data/{wallet_address}.json"
        if not os.path.exists(file_path):
            proxy = random.choice(reserv_proxies)
            process_wallet(wallet_address, proxy, reserv_proxies, results)

def menu():
    try:
        while True:
            action = select(
                "What do you want to do?",
                choices=[
                    Choice('💲 start stats MONAD', 'stats_monad'),
                    Choice('❌ Exit', 'exit')
                ],
                qmark='🛠️',
                pointer='👉'
            ).ask()

            if action == 'exit':
                break
            elif action == 'stats_monad':
                wallets, proxies = get_wallets_and_proxies()
                reserv_proxies = get_reserv_proxies()
                results = process_wallets(wallets, proxies, reserv_proxies)
                monad.process_results(results)
                process_json_to_csv()
                
    except Exception as e:
        log_error('Error: ' + str(e))

def main():
    menu()

main()