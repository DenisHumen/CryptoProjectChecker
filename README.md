# Layerhub Checker

### Пожертвование ``` TRC20 - TRWzXZE16bgJg3eHa9n8q4ioZjMgKHwF9a ```
<img src="usdt.jpg" alt="Donation" width="150"/>

Layerhub Checker - это инструмент на основе Python, предназначенный для проверки адресов кошельков в тестовой сети Monad с использованием прокси. Он извлекает информацию о кошельках и сохраняет результаты в формате JSON. Инструмент поддерживает многопоточность и ротацию прокси для обеспечения надежной и эффективной обработки.

Позже будет добавлен другой функционал на базе Layerhub.

## Особенности

- Поддержка многопоточности для более быстрой обработки
- Ротация прокси для обработки сбоев прокси
- Логирование ошибок в файл
- Настраиваемые параметры через файл TOML

## Требования

- Python 3.8+

## Установка

1. Клонируйте репозиторий:
    ```sh
    git clone https://github.com/yourusername/layerhub_checker.git
    cd layerhub_checker
    ```

2. Создайте виртуальное окружение и активируйте его:
    ```sh
    python3 -m venv .venv
    source .venv/bin/activate
    ```

3. Установите необходимые пакеты:
    ```sh
    pip install -r requirements.txt
    ```

## Конфигурация

Настройки конфигурации хранятся в файле `config/general_config.toml`. Вы можете настроить параметры по своему усмотрению.

```toml
THRENDS = 10
LIMIT_REPLACE_PROXY = 10

# Время задержки в секундах
SLEEP_BEATWEEN_WALLET = [1, 3]
SLEEP_BEATWEEN_REAPLECE_PROXY = [1, 3]
```

## Использование

1. Подготовьте файл `data/wallet.csv` в следующем формате:
    ```csv
    wallet_address,proxy
    0xED9ea229D863a41Ab1289Ea35D292Fe8dec*****,http://proxy1:port
    0xAnotherWalletAddress,http://proxy2:port
    ```

2. Подготовьте файл `data/reserv_proxy.csv` в следующем формате:
    ```csv
    http://reserveproxy1:port
    http://reserveproxy2:port
    ```

3. Запустите основной скрипт:
    ```sh
    python main.py
    ```

4. Следуйте подсказкам, чтобы начать проверку статистики или выйти из программы.

5. После каждого использования желательно очищать папку ```results/wallet_json_data``` если количество кошельков изменилось.

## Структура проекта

```
layerhub_checker/
├── config/
│   ├── general_config.toml
│   └── pyload_presset/
│       └── random_pyload.py
├── data/
│   ├── wallet.csv
│   └── reserv_proxy.csv
├── modules/
│   └── monad.py
├── results/
│   ├── logs/
│   │   └── log
│   └── wallet_json_data/
├── .venv/
├── main.py
└── README.md
```

## Логирование

Ошибки и важные сообщения записываются в файл `results/logs/log`. Это помогает в отладке и отслеживании прогресса выполнения скрипта.

## Ошибки 

```Error: Cannot choose from an empty sequence``` - добавь резервные прокси.

## Вклад

Вклады приветствуются! Пожалуйста, откройте issue или отправьте pull request для любых улучшений или исправлений ошибок.

## Лицензия

Этот проект лицензирован по лицензии MIT. См. файл `LICENSE` для получения дополнительной информации.