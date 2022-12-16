from main import vkinder
import json


def get_button(text, color):
    return {
        "action": {"type": "text",
                   "payload": "{\"button\": \"" + "1" + "\"}",
                   "label": f"{text}"
                   },
        "color": f"{color}"
           }


key = {
    "buttons": [
        [get_button('Начать поиск', 'positive')]
    ]
     }


def sender(user_id, text):
    vkinder.vk.method('messages.send', {'user_id': user_id,
                                        'message': text,
                                        'random_id': 0,
                                        'keyboard': key
                                        })


key = json.dumps(key, ensure_ascii=False).encode('utf-8')
key = str(key.decode('utf-8'))
