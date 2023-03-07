import discord
import openai
import asyncio
import requests
import os
from dotenv import load_dotenv

load_dotenv()

TEMPERATURE = 1.1
TOP_P = 0.8

openai.api_key = os.environ['OPEN_AI_TOKEN']
DEEPL_TOKEN = os.environ['DEEPL_TOKEN']
DISCORD_TOKEN = os.environ['DISCORD_TOKEN']

LANGUAGE_JAPAN = 'JA'
LANGUAGE_ENGLISH = 'EN'

DEEPL_URL = 'https://api-free.deepl.com/v2/translate'

OPEN_AI_MODEL = 'gpt-3.5-turbo'

BOT_WAKE_UP_MESSAGE = '起きた'

def translate(text, target_lang):

    params = {
            "auth_key": DEEPL_TOKEN,
            "text": text,
            "target_lang": target_lang
          }

    request = requests.post(DEEPL_URL, data=params)
    result = request.json()

    return result["translations"][0]["text"]

def generate_response(text):

    response = openai.ChatCompletion.create(
    model = OPEN_AI_MODEL,
    messages = [
        {"role": "user", "content": text}
    ],
    temperature = TEMPERATURE,
    top_p = TOP_P)

    return response["choices"][0]["message"]["content"]


# 接続に必要なオブジェクトを生成
client = discord.Client(intents=discord.Intents.all())

# 起動時に動作する処理
@client.event
async def on_ready():
    # 起動したらターミナルにログイン通知が表示される
    print(BOT_WAKE_UP_MESSAGE)

# 返信する非同期関数を定義
async def reply(message):

    input_text = message.clean_content
    input_text = input_text.replace(f"@{client.user.name} ", "")

    print(input_text)
    
    # input_text = translate(input_text, LANGUAGE_ENGLISH)

    reply = generate_response(input_text)

    # reply = translate(reply, LANGUAGE_JAPAN)
    
    await message.channel.send(reply) # 返信メッセージを送信

# 発言時に実行されるイベントハンドラを定義
@client.event
async def on_message(message):
    if client.user in message.mentions: # 話しかけられたかの判定
        await reply(message) # 返信する非同期関数を実行

# Botの起動とDiscordサーバーへの接続
client.run(DISCORD_TOKEN)