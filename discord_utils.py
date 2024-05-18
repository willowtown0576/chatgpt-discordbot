import discord
import os
from discord.ext import commands
from dotenv import load_dotenv


class DiscordClient:
    """
    Discordのサービスとやり取りを行うクライアント。
    """

    def __init__(self):
        """
        環境変数からAPIトークンを読み込んでDiscordClientを初期化します。
        """
        load_dotenv()
        self.DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
        self.intents = discord.Intents.default()
        self.intents.messages = True
        self.intents.message_content = True
        self.intents.voice_states = True
        self.bot = commands.Bot(command_prefix="/", intents=self.intents)

    def get_bot(self) -> commands.Bot:
        """
        Discordのボットインスタンスを返します。

        Returns:
            commands.Bot: Discordのボットインスタンス。
        """
        return self.bot
