import random

def random_pyload_presset():
    pyload1 = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "get_account",
        "params": "0x"
    },
    pyload2 = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "get_account",
        "params": "0x"
    }
    pyload3 = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "get_account",
        "params": "0x"
    }
    pyload4 = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "get_account",
        "params": "0x"
    }
    pyload5 = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "get_account",
        "params": "0x"
    }

    random_pyload = random.choice([pyload1, pyload2, pyload3, pyload4, pyload5])
    return random_pyload