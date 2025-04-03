import requests
import csv
import os
import json
from datetime import datetime
from tqdm import tqdm

def check_monad_eligibility(wallet_address, proxy):
    url = f"https://backend.gas.zip/v2/monadEligibility/{wallet_address}"
    headers = {
        "sec-ch-ua": "\"Not A(Brand\";v=\"8\", \"Chromium\";v=\"132\", \"Google Chrome\";v=\"132\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Linux\"",
        "referrer": "https://www.gas.zip/",
        "referrerPolicy": "strict-origin-when-cross-origin"
    }
    proxies = {
        "http": proxy,
        "https": proxy
    }
    
    try:
        response = requests.get(url, headers=headers, proxies=proxies)
        response.raise_for_status() 
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

def log_error(message):
    log_file_path = "results/logs/log"
    os.makedirs(os.path.dirname(log_file_path), exist_ok=True)  
    with open(log_file_path, 'a') as log_file:
        log_file.write(message + '\n')

def gaszip_monad_checker_process_wallets_from_csv():
    input_file_path = "data/wallet.csv" 
    output_dir = "results/wallet_json_data"
    os.makedirs(output_dir, exist_ok=True)  

    results = []
    try:
        with open(input_file_path, mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            rows = list(csv_reader)
            with tqdm(total=len(rows), desc="Processing wallets") as pbar:
                for row in rows:
                    wallet_address = row['wallet_address']
                    proxy = row['proxy']
                    try:
                        result = check_monad_eligibility(wallet_address, proxy)
                        results.append({"wallet_address": wallet_address, "result": result})
                        
                        output_file = os.path.join(output_dir, f"{wallet_address}.json")
                        with open(output_file, mode='w') as json_file:
                            json.dump(result, json_file, indent=4)
                    except Exception as e:
                        log_error(f"Error processing wallet {wallet_address}: {str(e)}")
                    finally:
                        pbar.update(1)
    except Exception as e:
        log_error(f"Error reading CSV file: {str(e)}")
    return results

def gaszip_monad_checker_export_json_to_csv():
    input_dir = "results/wallet_json_data"
    output_file = "results/result.csv"
    os.makedirs("results", exist_ok=True)  

    try:
        json_files = [f for f in os.listdir(input_dir) if f.endswith(".json")]
        with open(output_file, mode='w', newline='') as csv_file:
            fieldnames = ["wallet_address", "eligibility", "last_claim_time", "num_deposits", "reward_amount", "tx_hash"]
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()

            with tqdm(total=len(json_files), desc="Exporting to CSV") as pbar:
                for filename in json_files:
                    wallet_address = filename.replace(".json", "")
                    file_path = os.path.join(input_dir, filename)
                    try:
                        with open(file_path, mode='r') as json_file:
                            data = json.load(json_file)
                            last_claim_time = data.get("last_claim_time")
                            if last_claim_time:
                                last_claim_time = datetime.utcfromtimestamp(last_claim_time).strftime('%Y-%m-%d %H:%M:%S')
                            writer.writerow({
                                "wallet_address": wallet_address,
                                "eligibility": data.get("eligibility"),
                                "last_claim_time": last_claim_time,
                                "num_deposits": data.get("num_deposits"),
                                "reward_amount": data.get("reward_amount"),
                                "tx_hash": data.get("tx_hash")
                            })
                    except Exception as e:
                        log_error(f"Error processing JSON file {filename}: {str(e)}")
                    finally:
                        pbar.update(1)
    except Exception as e:
        log_error(f"Error exporting to CSV: {str(e)}")


