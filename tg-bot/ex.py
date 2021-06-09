import requests


# https://api.telegram.org/bot1860975146:AAHSU7SS4Mg4qDq6o-Wy2hjlu5mD-KMBB78/getUpdates
# https://api.telegram.org/bot1860975146:AAHSU7SS4Mg4qDq6o-Wy2hjlu5mD-KMBB78/sendMessage?chat_id=257186853&text=Hi

TOKEN = '1860975146:AAHSU7SS4Mg4qDq6o-Wy2hjlu5mD-KMBB78'
API_link = f'https://api.telegram.org/bot{TOKEN}'


def bot_updates(offset=None):
    if offset is not None:
        answer = requests.get(API_link + '/getUpdates' + f'?offset={offset}').json()
        print(answer)
    else:
        answer = requests.get(API_link + '/getUpdates').json()
        print(answer)

    message = answer['result'][0]['message']
    chat_id = message['from']['id']
    text = 'Вы написали: ' + message['text']

    bot_sendMessage(chat_id, text)


def bot_sendMessage(chat_id, text):
    request = requests.get(API_link + f'/sendMessage?chat_id={chat_id}&text={text}')
    # print(request.json())


# bot_sendMessage(257186853, 'Hey')
bot_updates(offset=-1)
