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

from modules.gel_all_json import clear_wallet_json_data
from modules.check_files import check_and_create_paths
from modules.megaeth import (
    process_wallets as process_megaeth_wallets,
    ensure_all_wallets_processed as ensure_all_megaeth_wallets_processed,
    process_results_to_csv as process_megaeth_results_to_csv
)

def monad():
    while True:
        # Основное меню для работы с MONAD
        action = select(
            "What do you want to do?",
            choices=[
                Choice('💲 Start stats MONAD', 'stats_monad'),
                Choice('🔍 GasZip monad faucet checker', 'gaszip_monad_faucet_checker'),
                Choice('🗑️ Clear wallet json data | Удалит все созданные json после запроса', 'clear_wallet_json_data'),
                Choice('🔙 Back', 'Back')
            ],
            qmark='🛠️',
            pointer='👉'
        ).ask()

        if action == 'Back':
            break
        elif action == 'stats_monad':
            # Получение данных кошельков и прокси
            wallets, proxies = get_wallets_and_proxies()
            reserv_proxies = get_reserv_proxies()
            
            # Загрузка конфигурации из TOML-файла
            config = toml.load('config/general_config.toml')
            num_threads = config.get('THRENDS', 10)
            sleep_between_wallet = config.get('SLEEP_BEATWEEN_WALLET', [1, 3])
            sleep_between_replace_proxy = config.get('SLEEP_BEATWEEN_REAPLECE_PROXY', [1, 3])
            limit_replace_proxy = config.get('LIMIT_REPLACE_PROXY', 10)
            
            # Обработка кошельков
            results = process_wallets(wallets, proxies, reserv_proxies, num_threads, sleep_between_wallet, sleep_between_replace_proxy, limit_replace_proxy)
            
            # Обработка и экспорт результатов
            process_results(results)
            process_json_to_csv()
        elif action == 'gaszip_monad_faucet_checker':
            # Проверка GasZip Monad Faucet
            gaszip_monad_checker_process_wallets_from_csv()
            gaszip_monad_checker_export_json_to_csv()
        elif action == 'clear_wallet_json_data':
            # Очистка данных JSON
            clear_wallet_json_data()

def megaeth():
    while True:
        # Основное меню для работы с MEGAETH
        action = select(
            "What do you want to do?",
            choices=[
                Choice('💲 Start stats MEGAETH', 'stats_megaeth'),
                Choice('🗑️ Clear wallet json data | Удалит все созданные json после запроса', 'clear_wallet_json_data'),
                Choice('🔙 Back', 'Back')
            ],
            qmark='🛠️',
            pointer='👉'
        ).ask()

        if action == 'Back':
            break
        elif action == 'stats_megaeth':
            # Получение данных кошельков и прокси
            wallets, proxies = get_wallets_and_proxies()
            reserv_proxies = get_reserv_proxies()
            
            # Загрузка конфигурации из TOML-файла
            config = toml.load('config/general_config.toml')
            num_threads = config.get('THRENDS', 30)
            sleep_between_wallet = config.get('SLEEP_BEATWEEN_WALLET', [1, 3])
            sleep_between_replace_proxy = config.get('SLEEP_BEATWEEN_REAPLECE_PROXY', [1, 3])
            limit_replace_proxy = config.get('LIMIT_REPLACE_PROXY', 10)
            
            # Обработка кошельков
            results = process_megaeth_wallets(wallets, proxies, reserv_proxies, num_threads, sleep_between_wallet, sleep_between_replace_proxy, limit_replace_proxy)
            
            # Убедиться, что все кошельки обработаны
            ensure_all_megaeth_wallets_processed(wallets, proxies, reserv_proxies, results, sleep_between_replace_proxy, limit_replace_proxy)
            
            # Сохранение результатов в CSV
            process_megaeth_results_to_csv(results)
        elif action == 'clear_wallet_json_data':
            # Очистка данных JSON
            clear_wallet_json_data()

def menu():
    # Проверка и создание необходимых путей
    check_and_create_paths()
    try:
        # Основное меню
        while True:
            action = select(
                "What do you want to do?",
                choices=[
                    Choice('💲 MONAD', 'monad'),
                    Choice('💲 MEGAETH', 'megaeth'),
                    Choice('❌ Exit', 'exit')
                ],
                qmark='🛠️',
                pointer='👉'
            ).ask()

            if action == 'exit':
                break
            elif action == 'monad':
                monad()
            elif action == 'megaeth':
                megaeth()
    except Exception as e:
        # Обработка ошибок
        print(f"Error: {str(e)}")

def main():
    menu()

main()