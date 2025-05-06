import requests
import time

# Новый запрос к API
blockscout_url = "https://soneium.blockscout.com/api/v2/addresses/0x50dB159B6C19AC96BF4734E8f6a7404cb3456245/nft/collections?type=ERC-1155"
blockscout_headers = {
    "accept": "*/*",
    "accept-language": "ru,en-US;q=0.9,en;q=0.8",
    "priority": "u=1, i",
    "sec-ch-ua": '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Linux"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "cross-site"
}

# Прокси
proxy_host = ""
proxy_port = ""
proxy_user = ""
proxy_pass = ""

proxy_url = f"http://{proxy_user}:{proxy_pass}@{proxy_host}:{proxy_port}"
proxies = {
    "http": proxy_url,
    "https": proxy_url
}

print("[1] Отправка запроса к Blockscout API через прокси...")
try:
    blockscout_response = requests.get(blockscout_url, headers=blockscout_headers, proxies=proxies, timeout=15)
    blockscout_response.raise_for_status()
    blockscout_data = blockscout_response.json()
    print("[+] Ответ от Blockscout API:", blockscout_data)
except requests.exceptions.RequestException as e:
    print(f"[!] Ошибка при выполнении запроса к Blockscout API: {e}")
    blockscout_data = {}
except ValueError:
    print("[!] Ошибка: Ответ от Blockscout API не является корректным JSON.")
    blockscout_data = {}

# Список всех URL-запросов
wallet = ''

urls = [
    f'https://soneium-mainnet.g.alchemy.com/nft/v3/T8CMKWYTV1VEdNusi5sz1M2o67ZFOnLR/isHolderOfContract?wallet={wallet}&contractAddress=0x8918531fC73f2c9047f0163eA126EeD1B8EA2c63',
    f'https://soneium-mainnet.g.alchemy.com/nft/v3/kdP7I6BPv7RcZGjrVqzLexheN0IpEhas/isHolderOfContract?wallet={wallet}&contractAddress=0x391Dece93d18Fca922bF337C25Ee38BeA74Db63E',
    f'https://soneium-mainnet.g.alchemy.com/nft/v3/KyKYbjCKozmpH-w2SD93nj14cSS9y18G/isHolderOfContract?wallet={wallet}&contractAddress=0x44EEfAC1D5Db283B2dD99e226B864da271D82952',
    f'https://soneium-mainnet.g.alchemy.com/nft/v3/aiTDFDCha4SeuArfU0mnbTgwbhlgbxH-/isHolderOfContract?wallet={wallet}&contractAddress=0x7A475a650a4867577cf488E94ec023E593997fd6',
    f'https://soneium-mainnet.g.alchemy.com/nft/v3/sN1RDdsGjnrTLlQnWJshrkzjYJAEV0JO/isHolderOfContract?wallet={wallet}&contractAddress=0x39C5DfF4e39779492C3AE3898c8d5a0579fE684e',
    f'https://soneium-mainnet.g.alchemy.com/nft/v3/Ctxdv-oWvvtKz_2ESo8q4LI7vEA7UJ-T/isHolderOfContract?wallet={wallet}&contractAddress=0x670113b4AE5416E1368669bE1cdcc918871827eA',
    f'https://soneium-mainnet.g.alchemy.com/nft/v3/KyKYbjCKozmpH-w2SD93nj14cSS9y18G/isHolderOfContract?wallet={wallet}&contractAddress=0x4591D540B692CBeD60Db7781B7683910f7a3BF8C',
    f'https://soneium-mainnet.g.alchemy.com/nft/v3/FBKOVxVYW0yobV1ntzs7u5qM0E6_xRwO/isHolderOfContract?wallet={wallet}&contractAddress=0x5C0221a8c3eB5956b70cDC572fA0F6C952274f1A',
    f'https://soneium-mainnet.g.alchemy.com/nft/v3/sN1RDdsGjnrTLlQnWJshrkzjYJAEV0JO/isHolderOfContract?wallet={wallet}&contractAddress=0x3a634e6f8C2bf2C5894722B908d99e3cF9C62eD3',
    f'https://soneium-mainnet.g.alchemy.com/nft/v3/KyKYbjCKozmpH-w2SD93nj14cSS9y18G/isHolderOfContract?wallet={wallet}&contractAddress=0x6DD843fe15dbFD41F001d448cb246ac8b65a6027',
    f'https://soneium-mainnet.g.alchemy.com/nft/v3/rz6gptgOC1RV06rJL7389sJl4hrdO3tQ/isHolderOfContract?wallet={wallet}&contractAddress=0x4A33e2E308E5d9C0188d209F1bF443Ff7CfB4A31',
    f'https://soneium-mainnet.g.alchemy.com/nft/v3/CYNsauBQGJ72SA0qDdTdcIo0PW5lecQb/isHolderOfContract?wallet={wallet}&contractAddress=0x066ABA7c3520e300113C0515FF41c084eE0c95Ea',
    f'https://soneium-mainnet.g.alchemy.com/nft/v3/sN1RDdsGjnrTLlQnWJshrkzjYJAEV0JO/isHolderOfContract?wallet={wallet}&contractAddress=0x55E906C6Fb98894f05E1a7A533d77732B79a5414',
    f'https://soneium-mainnet.g.alchemy.com/nft/v3/aiTDFDCha4SeuArfU0mnbTgwbhlgbxH-/isHolderOfContract?wallet={wallet}&contractAddress=0x0DEc30Af3551161606282a6bc1243526b6a3D1E9',
    f'https://soneium-mainnet.g.alchemy.com/nft/v3/sN1RDdsGjnrTLlQnWJshrkzjYJAEV0JO/isHolderOfContract?wallet={wallet}&contractAddress=0xcf87B2d5Ab008D41159f6737E2a5b6a3Bc40b753',
    f'https://soneium-mainnet.g.alchemy.com/nft/v3/kdP7I6BPv7RcZGjrVqzLexheN0IpEhas/isHolderOfContract?wallet={wallet}&contractAddress=0x2DCD9B33F0721000Dc1F8f84B804d4CFA23d7713',
    f'https://soneium-mainnet.g.alchemy.com/nft/v3/Ctxdv-oWvvtKz_2ESo8q4LI7vEA7UJ-T/isHolderOfContract?wallet={wallet}&contractAddress=0x4a3b67b339c272fAb639B0CAF3Ce7852B2Aa0833',
    f'https://soneium-mainnet.g.alchemy.com/nft/v3/T8CMKWYTV1VEdNusi5sz1M2o67ZFOnLR/isHolderOfContract?wallet={wallet}&contractAddress=0x83A0C5D831E7869f4c710658CBD1b455Ba92ad00',
    f'https://soneium-mainnet.g.alchemy.com/nft/v3/sN1RDdsGjnrTLlQnWJshrkzjYJAEV0JO/isHolderOfContract?wallet={wallet}&contractAddress=0xeAF42993E44be62c9113161c0016821C6A540B92',
    f'https://soneium-mainnet.g.alchemy.com/nft/v3/rz6gptgOC1RV06rJL7389sJl4hrdO3tQ/isHolderOfContract?wallet={wallet}&contractAddress=0x11B2876C58cFb7501Db60d0112AF8A8EfEB0A81D',
    f'https://soneium-mainnet.g.alchemy.com/nft/v3/rz6gptgOC1RV06rJL7389sJl4hrdO3tQ/isHolderOfContract?wallet={wallet}&contractAddress=0xAa6c38A85e5781bCc410693B52F64EfF1aFcd3c6',
    f'https://soneium-mainnet.g.alchemy.com/nft/v3/Ctxdv-oWvvtKz_2ESo8q4LI7vEA7UJ-T/isHolderOfContract?wallet={wallet}&contractAddress=0x1eC6AACC79f3c4817d7fea2268e1c54C6b2662Fb',
    f'https://soneium-mainnet.g.alchemy.com/nft/v3/T8CMKWYTV1VEdNusi5sz1M2o67ZFOnLR/isHolderOfContract?wallet={wallet}&contractAddress=0xc59f0D1B1b614d8446dDe1760fc3e6ae57bF9501',
    f'https://soneium-mainnet.g.alchemy.com/nft/v3/rz6gptgOC1RV06rJL7389sJl4hrdO3tQ/isHolderOfContract?wallet={wallet}&contractAddress=0x1833e394D879D9b493cdb0fe754F304f2E9F23bf',
    f'https://soneium-mainnet.g.alchemy.com/nft/v3/rz6gptgOC1RV06rJL7389sJl4hrdO3tQ/isHolderOfContract?wallet={wallet}&contractAddress=0x9d83A657581A966aDf1c346dAfEe3EBe258EC26D',
    f'https://soneium-mainnet.g.alchemy.com/nft/v3/rz6gptgOC1RV06rJL7389sJl4hrdO3tQ/isHolderOfContract?wallet={wallet}&contractAddress=0x7e058E9eeb81758F80049d0F2c1C1A7b47919697',
    f'https://soneium-mainnet.g.alchemy.com/nft/v3/FBKOVxVYW0yobV1ntzs7u5qM0E6_xRwO/isHolderOfContract?wallet={wallet}&contractAddress=0x690B97980877b5d7915E89E6D0Cb9748A8bdAB8d',
    f'https://soneium-mainnet.g.alchemy.com/nft/v3/sN1RDdsGjnrTLlQnWJshrkzjYJAEV0JO/isHolderOfContract?wallet={wallet}&contractAddress=0x890a19A1Dd75AAEcc4eDFce4685bb59C8ABEe78A',
    f'https://soneium-mainnet.g.alchemy.com/nft/v3/Ctxdv-oWvvtKz_2ESo8q4LI7vEA7UJ-T/isHolderOfContract?wallet={wallet}&contractAddress=0xCA707D22E248740aDaA9C63580F7A35201B18d30',
    f'https://soneium-mainnet.g.alchemy.com/nft/v3/kdP7I6BPv7RcZGjrVqzLexheN0IpEhas/isHolderOfContract?wallet={wallet}&contractAddress=0x9a4cC369A91AE5e8cBd99163a2eAC5b7957879dB'
]


# Заголовки запроса
headers = {
    "accept": "application/json",
    "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "ru,en-US;q=0.9,en;q=0.8",
    "origin": "https://cryptowalletsx.com",
    "priority": "u=1, i",
    "referer": "https://cryptowalletsx.com/",
    "sec-ch-ua": '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Linux"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "cross-site",
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"
}

# Прокси
proxy_host = "154.6.26.154"
proxy_port = "42328"
proxy_user = "761FL24L"
proxy_pass = "LO5VG6UA"

proxy_url = f"http://{proxy_user}:{proxy_pass}@{proxy_host}:{proxy_port}"
proxies = {
    "http": proxy_url,
    "https": proxy_url
}

# Обход всех URL-ов
for index, url in enumerate(urls, start=1):
    print(f"\n[{index}] Отправка запроса к:\n{url}")
    try:
        response = requests.get(url, headers=headers, proxies=proxies, timeout=15)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"[!] Ошибка при выполнении запроса: {e}")
        continue

    # Обработка JSON-ответа
    try:
        data = response.json()
        print("[+] Ответ от API:", data)
    except ValueError:
        print("[!] Ошибка: Ответ от API не является корректным JSON.")
        print(response.text)

    # Пауза между запросами
    time.sleep(1)  # можно увеличить до 2–3 сек при необходимости
