import requests
from colorama import Fore, Style
import json
from config.pyload_presset.random_pyload import random_pyload_presset

log_file_path = 'results/logs/log'

def log_error(message):
    with open(log_file_path, 'a') as log_file:
        log_file.write(message + '\n')

def monad_checker(wallet_address, proxy, pyload):
    if pyload is not None:
        try:
            url = f'https://layerhub.xyz/chains/monad_testnet/wallets/{wallet_address}'
            params = {"_rsc": "1bw6b"}
            headers = {
                "accept": "*/*",
                "accept-language": "ru,en-US;q=0.9,en;q=0.8",
                "next-router-state-tree": '%5B%22%22%2C%7B%22children%22%3A%5B%22(mainLayout)%22%2C%7B%22children%22%3A%5B%22search%22%2C%7B%22children%22%3A%5B%22__PAGE__%3F%7B%5C%22p%5C%22%3A%5C%22monad_testnet%5C%22%7D%22%2C%7B%7D%2C%22%2Fsearch%3Fp%3Dmonad_testnet%22%2C%22refresh%22%5D%7D%2Cnull%2Cnull%5D%7D%2Cnull%2Cnull%5D%7D%2Cnull%2Cnull%2Ctrue%5D',
                "next-url": "/search",
                "rsc": "1",
                "sec-ch-ua": "\"Not A(Brand\";v=\"8\", \"Chromium\";v=\"132\", \"Google Chrome\";v=\"132\"",
                "sec-ch-ua-mobile": "?0",
                "sec-ch-ua-platform": "\"Linux\"",
                "sec-fetch-dest": "empty",
                "sec-fetch-mode": "cors",
                "sec-fetch-site": "same-origin",
                "Referer": "https://layerhub.xyz/search?p=monad_testnet",
                "Referrer-Policy": "strict-origin-when-cross-origin"
            }

            response = requests.get(url, params=params, headers=headers, proxies={"http": proxy, "https": proxy})
            
            if response.status_code != 200:
                log_error(f'HTTP error: {response.status_code} - {response.text}')
                raise ValueError(f'HTTP error: {response.status_code}')
            
            if not response.content:
                log_error('Empty response content')
                raise ValueError('Empty response content')
            
            try:
                data = response.json()
                if isinstance(data, dict) and data.get("message") == "Wallet is not found for chain_id: monad_testnet":
                    log_error("Wallet not found, retrying...")
                    raise ValueError("Wallet not found, retrying...")
                data['wallet_address'] = wallet_address
            except json.JSONDecodeError:
                data = {"wallet_address": wallet_address, "response": response.text}
            
            return data
        
        except requests.exceptions.ProxyError as e:
            log_error('Proxy error: ' + str(e))
            raise e
        except requests.exceptions.RequestException as e:
            log_error('Request error: ' + str(e))
            raise e
        except Exception as e:
            log_error('Error: ' + str(e))
            raise e

    else:
        log_error('Error: No pyload found')

def process_results(results):
    for result in results:
        wallet_address = result.get('wallet_address', 'unknown_wallet')
        file_path = f"results/wallet_json_data/{wallet_address}.json"
        with open(file_path, 'w') as json_file:
            json.dump(result, json_file)