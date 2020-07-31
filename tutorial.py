import random
import configparser
from typing import Optional, List, Any, Union

from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError
from telethon.sync import TelegramClient
from telethon import functions, types

from pip._vendor import requests

# Reading Configs
config = configparser.ConfigParser()
config.read("config.ini")

api_id = config['Telegram']['api_id']
api_hash = config['Telegram']['api_hash']


phone = config['Telegram']['phone']
username = config['Telegram']['username']
client = TelegramClient(username, api_id, api_hash)


url= "https://api.telegram.org/bot1175948210:AAGOeRPG3F743SbQbDSqkZg-etr-gMyqgMI/"

# create func that get chat id
def get_chat_id(update):
    chat_id = update['message']["chat"]["id"]
    return chat_id


# create function that get message text
def get_message_text(update):
    message_text = update["message"]["text"]
    return message_text


# create function that get last_update
def last_update(req):
    response = requests.get(req + "getUpdates")
    response = response.json()
    result = response["result"]
    total_updates = len(result) - 1
    return result[total_updates]  # get last record message update


# create function that let bot send message to user
def send_message(chat_id, message_text):
    params = {"chat_id": chat_id, "text": message_text, "parse_mode": 'HTML'}
    response = requests.post(url + "sendMessage", data=params)
    return response


def concatenate_list_data(list):

    groups = []
    html = '<b>Company Name</b>\n'
    html = html+'<b>Company URL/Info</b>\n'
    html = html+ '<b>Advertisement</b>\n'
    i=1
    for i,x in enumerate(list.chats,start=1):
        html=html+"{}.{}".format(i,' <a href="https://t.me/'+x.username+'"><b>' + x.title + '</b></a>\n')

    return html


async def main():
    await client.start()
    #await client.send_message('me', 'Type a keyword to search channels/groups')
   # await client.send_message('me', 'Type a keyword to search channels/groups')
   # print(result.chats[0].id)

    update_id = last_update(url)["update_id"]
    while True:
        update = last_update(url)
        #send_message(get_chat_id(update), 'Type a keyword to search channels/groups')
        if update_id == update["update_id"]:

            if get_message_text(update).lower() != ""  or get_message_text(update) != "Type a keyword to search channels/groups":
                search = get_message_text(update).lower()
                result: Union[List[Optional[Any]], Any] = await client(functions.contacts.SearchRequest(
                    q=search,
                    limit=100
                ))

                #print(result.stringify())
                send_message(get_chat_id(update), concatenate_list_data(result))
            elif get_message_text(update).lower() == "play":
                _1 = random.randint(1, 6)
                _2 = random.randint(1, 6)
                _3 = random.randint(1, 6)
                send_message(get_chat_id(update),
                             'You have ' + str(_1) + ' and ' + str(_2) + ' and ' + str(_3) + ' !\n Your result is ' +
                             str(_1 + _2 + _3) + '!!!')
            else:
                send_message(get_chat_id(update), "Sorry Not Understand what you inputted:( I love you")
            update_id += 1

with client:
    client.loop.run_until_complete(main())











