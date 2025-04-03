import os
from colorama import Fore, Style

def ensure_path_exists(path, is_file=False, created_items=None):
    if is_file:
        if not os.path.exists(path):
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, 'w') as f:
                pass
            if created_items is not None:
                created_items.append(path)
    else:
        if not os.path.exists(path):
            os.makedirs(path, exist_ok=True)
            if created_items is not None:
                created_items.append(path)

def check_and_create_paths():
    paths = {
        "data/reserv_proxy.csv": True,
        "data/wallet.csv": True,
        "results/logs/log": True,
        "results/result.csv": True,
        "data": False,
        "results": False,
        "results/wallet_json_data": False
    }

    created_items = []

    for path, is_file in paths.items():
        ensure_path_exists(path, is_file, created_items)

    if created_items:
        print(Fore.GREEN + Style.BRIGHT + "\n\n✅ Created the following items:" + Style.RESET_ALL)
        for item in created_items:
            print(Fore.GREEN + f"  - {item}" + Style.RESET_ALL)
    else:
        print(Fore.GREEN + Style.BRIGHT + "\n\n✅ All required items already exist." + Style.RESET_ALL)
