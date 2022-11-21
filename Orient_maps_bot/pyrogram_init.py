import asyncio
from pyrogram import Client


with open('telegram_api_params.txt') as f:
    api_params_raw = f.read().strip()
api_params = dict()
for param in api_params_raw.split('\n'):
    api_params[param.split(':')[0]] = param.split(':')[1]

with open('Orient_maps_bot/telebot_token.txt') as f:
    bot_token = f.read().strip()


with Client("my_bot", api_params['api_id'], api_params['api_hash'], bot_token) as app:
    app.run()
