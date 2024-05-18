import discord
from discord.ext import commands
import os
import re
from dotenv import load_dotenv
import openai_utils as gpt

# .envファイルから環境変数を読み取る
load_dotenv()

# 環境変数から以下を取得
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.voice_states = True
bot = commands.Bot(command_prefix="/", intents=intents)

openai_client = gpt.OpenAiClient()


@bot.event
async def on_ready() -> None:
    """起動時に実行される関数"""
    print(f"{bot.user} has connected to Discord!")


@bot.event
async def on_message(message: discord.Message) -> None:
    """テキストメッセージ送信時に実行される関数

    Args:
        message (discord.Message): メッセージ内容
    """
    # Bot自身のメッセージは無視
    if message.author == bot.user:
        return

    # メンションされた場合のみ反応
    if bot.user.mentioned_in(message) and message.mention_everyone is False:
        user_id = message.author.id
        prompt_text = re.sub(f"<@!?{bot.user.id}>", "", message.content).strip()
        reply_message = openai_client.send_message(user_id, prompt_text)
        await message.reply(reply_message)

    # コマンドの処理
    await bot.process_commands(message)


@bot.command()
async def join(ctx: commands.Context) -> None:
    """ボイスチャット参加時に実行する関数

    Args:
        ctx (commands.Context): コンテキストオブジェクト
    """
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        try:
            voice_client = await channel.connect()
            await ctx.send(f'ボイスチャンネル"{channel.name}"に参加しました')
            # while voice_client.is_connected():
            #     if voice_client.is_paused():
            #         continue
            #     user_voice_filename = audio_utils.recording_audio(voice_client)
            #     file_size = Path(user_voice_filename).stat().st_size
            #     if file_size > 500:
            #         user_voice_transcript = openai_client.speech_to_text(
            #             user_voice_filename
            #         )
            #         reply_message = openai_client.send_message(
            #             ctx.author.id, user_voice_transcript
            #         )
            #         reply_voice_filename = openai_client.text_to_speech(reply_message)
            #         voice_client.play(
            #             discord.FFmpegPCMAudio(reply_voice_filename),
            #             after=lambda e: os.remove(reply_voice_filename),
        except Exception as e:
            await ctx.send(f"エラーが発生しました: {e}")
            print(f"Error: {e}")
    else:
        await ctx.send("あなたはまだボイスチャンネルに接続していません")


@bot.command()
async def hey(ctx: commands.Context, *, text: str) -> None:
    if ctx.voice_client:
        reply_message = openai_client.send_message(ctx.author.id, text)
        reply_voice_filename = openai_client.text_to_speech(reply_message)
        ctx.voice_client.play(discord.FFmpegPCMAudio(reply_voice_filename))
        await ctx.send(reply_message)
    else:
        await ctx.send("ボイスチャンネルに接続していません。")


@bot.command()
async def bye(ctx: commands.Context) -> None:
    """ボイスチャンネル退出時に実行する関数

    Args:
        ctx (commands.Context): コンテキストオプジェクト
    """
    if ctx.voice_client:
        await ctx.voice_client.disconnect()


bot.run(DISCORD_TOKEN)
