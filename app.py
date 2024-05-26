import discord
from discord.ext import commands
import re
import discord_client as dc
import openai_client as oc


discord_client = dc.DiscordClient()
openai_client = oc.OpenAiClient()
bot = discord_client.get_bot()


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
        await channel.connect()
        await ctx.send(f'ボイスチャンネル"{channel.name}"に参加しました')
    else:
        await ctx.send("あなたはまだボイスチャンネルに接続していません")


@bot.command()
async def hey(ctx: commands.Context, *, text: str) -> None:
    """テキストに対する応答を音声で実施するための関数

    Args:
        ctx (commands.Context): コンテキストオブジェクト
        text (str): AIに投げるテキスト
    """
    if ctx.voice_client:
        reply_message = openai_client.send_message(ctx.author.id, text)
        reply_message_audio = discord.FFmpegPCMAudio(
            openai_client.text_to_speech(reply_message)
        )
        ctx.voice_client.play(reply_message_audio)
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


if __name__ == "__main__":
    bot.run(discord_client.DISCORD_TOKEN)
