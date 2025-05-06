import json
import csv
import os
import requests
import shutil

TMP_DIR = 'tmp'

def fetch_town_data(output_file=f'{TMP_DIR}/town_raw_stats.json'):
    """Fetch data from the Dune API and save it to the tmp directory in chunks."""
    os.makedirs(TMP_DIR, exist_ok=True)
    url = 'https://api.dune.com/api/v1/query/4887195/results?'
    headers = {'X-Dune-API-Key': 'ObYyt7QK2Gz8ZepZbDjRtkQu75RSs3vl'}
    
    with requests.get(url, headers=headers, stream=True) as response:
        response.raise_for_status()  # Raise an error for bad responses
        with open(output_file, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):  # Stream data in chunks
                f.write(chunk)
    #print(f"Data fetched and saved to {output_file}")

def process_town_stats(wallets_file='data/wallet.csv', json_file=f'{TMP_DIR}/town_raw_stats.json', output_file='results/result.csv'):
    """Process town stats by matching wallets with fetched JSON data."""
    # Load wallets from wallets_file
    with open(wallets_file, 'r') as wf:
        wallets = [line.split(',')[0].strip().lower() for line in wf]  # Extract wallet addresses and normalize

    # Load JSON data from json_file
    with open(json_file, 'r') as jf:
        try:
            data = json.load(jf)  
            data = data.get('result', {}).get('rows', [])
        except json.JSONDecodeError as e:
            #print(f"Error decoding JSON: {e}")
            data = []

    wallet_data = {
        entry['wallet_address'].strip().lower(): entry
        for entry in data
        if isinstance(entry, dict) and 'wallet_address' in entry
    }

    # Write results to output_file
    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['wallet_address', 'leaderboard_rank', 'total_Tipped_ETH'])  

        for wallet in wallets:
            if wallet in wallet_data:
                entry = wallet_data[wallet]
                writer.writerow([wallet, entry.get('leaderboard_rank', 'None'), entry.get('total_Tipped_ETH', 'None')])
            else:
                writer.writerow([wallet, 'None', 'None'])

def run_town_stats():
    """Fetch, process, and clean up town stats."""
    try:
        fetch_town_data()
        process_town_stats()
    finally:
        if os.path.exists(TMP_DIR):
            shutil.rmtree(TMP_DIR)
            #print(f"Temporary directory '{TMP_DIR}' cleaned up.")