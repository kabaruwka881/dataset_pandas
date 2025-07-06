import requests

url = "https://api.intelligence.io.solutions/api/v1/chat/completions"
model_name = "meta-llama/Llama-4-Maverick-17B-128E-Instruct-FP8"
cached_key = None

def load_api_keys():
    with open('ai_access/api_key.txt', 'r') as f:
        return [line.strip() for line in f if line.strip()]

def test_api_key(api_key):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }
    test_message = {
        "model": model_name,
        "messages": [
            {
                "role": "user",
                "content": "ping"
            }
        ]
    }
    try:
        response = requests.post(url, headers=headers, json=test_message, timeout=10)
        return response.status_code == 200
    except requests.RequestException:
        return False

def get_working_api_key(api_keys):
    global cached_key
    if cached_key:
        return cached_key
    for key in api_keys:
        print(f"[ПРОВЕРКА] Пробуем ключ: {key[:25]}...")
        if test_api_key(key):
            print(f"[УСПЕХ] Рабочий ключ найден: {key[:25]}...")
            cached_key = key
            return key
        else:
            print(f"[ОТКАЗ] Ключ не сработал.")
    raise RuntimeError("[ОШИБКА] Нет рабочих API ключей")


def get_chat_answer_llama(message):
    keys = load_api_keys()
    api_keys = load_api_keys()
    api_key = get_working_api_key(api_keys)

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }
    data = {
        "model": model_name,
        "messages": [
            {
                "role": "user",
                "content": message
            }
        ]
    }
    print('[ОБРАБОТКА] Запрос был отправлен.')
    response = requests.post(url, headers=headers, json=data)
    if response.status_code != 200:
        print(f"[ОШИБКА] Ответ {response.status_code}, повторная попытка с другим ключом...")
        global cached_key
        cached_key = None
        return get_chat_answer_llama(message)
    return response.json()['choices'][0]['message']['content']
