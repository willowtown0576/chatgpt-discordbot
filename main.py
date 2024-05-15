import discord
from openai import OpenAI
from dotenv import load_dotenv
import os
import re

# .envファイルから環境変数を読み取る
load_dotenv()

# 環境変数からDiscord BotのトークンとOpenAIのAPIキーを取得
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
GPT_MODEL = os.getenv('GPT_MODEL')
GPT_ROLE = os.getenv('GPT_ROLE')

# Discordクライアントの初期化
intents = discord.Intents.default()
intents.messages = True
discord_client = discord.Client(intents=intents)

# OpenAIクライアントの初期化
openai_client = OpenAI(api_key=OPENAI_API_KEY)

# ユーザごとの会話履歴を保持する辞書
conversation_history = {}

@discord_client.event
async def on_ready():
    print(f'{discord_client.user} has connected to Discord!')

@discord_client.event
async def on_message(message):
    # Bot自身のメッセージは無視
    if message.author == discord_client.user:
        return
    
    # メンションされた場合のみ反応
    if discord_client.user.mentioned_in(message) and message.mention_everyone is False:
        # ユーザIDを取得
        user_id = message.author.id
        
        # メンションを除いたメッセージ内容をプロンプトとして使用
        prompt_text = re.sub(f"<@!?{discord_client.user.id}>", '', message.content).strip()
        
        # ユーザごとの履歴を取得または初期化
        if user_id not in conversation_history:
            conversation_history[user_id] = []
        
        # 現在のユーザのメッセージを履歴に追加
        conversation_history[user_id].append({"role": "user", "content": prompt_text})

        # ChatGPT APIを実行
        response = openai_client.chat.completions.create(
            model=GPT_MODEL,
            messages=[
                {"role": "system", "content": GPT_ROLE},
                *conversation_history[user_id]
            ]
        )

        # Botの応答を履歴に追加
        conversation_history[user_id].append({"role": "assistant", "content": response.choices[0].message.content})

        # メッセージに応答
        await message.reply(response.choices[0].message.content)

discord_client.run(DISCORD_TOKEN)
