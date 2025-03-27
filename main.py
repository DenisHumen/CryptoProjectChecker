import toml
from questionary import Choice, select
from modules.monad import (
    get_wallets_and_proxies,
    get_reserv_proxies,
    process_wallets,
    process_results,
    process_json_to_csv
)
from modules.gaszip_monad_faucet_checker import (
    gaszip_monad_checker_process_wallets_from_csv,
    gaszip_monad_checker_export_json_to_csv
)

def menu():
    try:
        while True:
            action = select(
                "What do you want to do?",
                choices=[
                    Choice('💲 start stats MONAD', 'stats_monad'),
                    Choice('🔍 gaszip monad faucet checker', 'gaszip_monad_faucet_checker'),
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
                config = toml.load('config/general_config.toml')
                num_threads = config.get('THRENDS', 10)
                sleep_between_wallet = config.get('SLEEP_BEATWEEN_WALLET', [1, 3])
                sleep_between_replace_proxy = config.get('SLEEP_BEATWEEN_REAPLECE_PROXY', [1, 3])
                limit_replace_proxy = config.get('LIMIT_REPLACE_PROXY', 10)
                
                results = process_wallets(wallets, proxies, reserv_proxies, num_threads, sleep_between_wallet, sleep_between_replace_proxy, limit_replace_proxy)
                process_results(results)
                process_json_to_csv()
            elif action == 'gaszip_monad_faucet_checker':
                gaszip_monad_checker_process_wallets_from_csv()
                gaszip_monad_checker_export_json_to_csv()
    except Exception as e:
        print(f"Error: {str(e)}")

def main():
    menu()

main()