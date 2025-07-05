#meta-llama/Llama-4-Maverick-17B-128E-Instruct-FP8

import requests

url = "https://api.intelligence.io.solutions/api/v1/chat/completions"
api_key = 'io-v2-eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJvd25lciI6Ijk3ZmMxNjM1LTJjYTMtNGU2Mi1iYTc3LTBlZmNkYmFkMDlkMiIsImV4cCI6NDkwNTE0OTA4MH0.oUq1-bwqHD2qwxSt0JBMSeuLu0wh7VAUjqbxlFN4sqCr9VfkFsBa4DH9DSp41DWHxc2pSM4MQtyp7vYh23PLWA'

def get_chat_answer_llama(message):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }
    data = {
        "model": "meta-llama/Llama-4-Maverick-17B-128E-Instruct-FP8",
        "messages": [
            {
                "role": "user",
                "content": message
            }
        ]
    }
    print('[ОБРАБОТКА] Запрос был отправлен.')
    response = requests.post(url, headers=headers, json=data)
    data = response.json()

    text = data['choices'][0]['message']['content']
    return text

