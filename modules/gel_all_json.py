import os
import platform
import shutil
from tqdm import tqdm
from colorama import Fore, Style
from questionary import Choice, select

def clear_wallet_json_data():
    while True:
        action = select(
            "❌ Удалить?",
            choices=[
                Choice('✅ YES', 'YES'),
                Choice('❌ NO', 'NO'),
            ],
            qmark='🛠️',
            pointer='👉'
        ).ask()

        if action == 'NO':
            break
        elif action == 'YES':
            base_dir = os.path.dirname(os.path.abspath(__file__))
            target_dir = os.path.join(base_dir, "../results/wallet_json_data")
            
            if not os.path.exists(target_dir):
                print(Fore.RED + f"❌ Directory {target_dir} does not exist." + Style.RESET_ALL)
                return

            items = os.listdir(target_dir)
            
            for item in tqdm(items, desc="Deleting files", unit="file"):
                item_path = os.path.join(target_dir, item)
                try:
                    if os.path.isfile(item_path) or os.path.islink(item_path):
                        os.unlink(item_path)  
                    elif os.path.isdir(item_path):
                        shutil.rmtree(item_path)  
                except Exception as e:
                    print(Fore.YELLOW + f"⚠️ Failed to delete {item_path}: {e}" + Style.RESET_ALL)

            print(Fore.GREEN + Style.BRIGHT + "\n\n✅ Deletion process completed." + Style.RESET_ALL)
            break