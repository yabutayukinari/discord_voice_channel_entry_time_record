import re
from datetime import datetime, timedelta, timezone

import discord
from discord.ext import commands
from discord.ext.commands.errors import (
    BadArgument,
    TooManyArguments,
    MissingRequiredArgument
)

from services.voice_channel_service import *


class AddVoiceChannel(commands.Cog):

    CHANNEL_TYPE_TEXT = 0
    CHANNEL_TYPE_VOICE = 2

    JST = timezone(timedelta(hours=+9), 'JST')

    def __init__(self, bot):
        self.bot = bot
        self.voice_channel_service = VoiceChannelService()

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def add_voice_channel(self, ctx, discord_id: int, is_record: int):
        """
        ボイスチャンネル登録
        権限チェックが欲しいところ
        :param ctx:
        :param discord_id:
        :param is_record:
        :return:
        """

        if self.validate(discord_id, is_record) is False:
            logger.info('チャンネル登録 失敗： 入力エラー')
            embed = discord.Embed(title="メンバー登録", description="入力値を確認してください。", color=0xc0392b)
            embed.add_field(name='discord_id', value=str(discord_id), inline=False)
            embed.add_field(name='is_record', value=str(is_record), inline=False)
            await ctx.send(embed=embed)
            return

        # 現在日時
        now = datetime.now(self.JST)
        self.save_voice_channel(discord_id,is_record, now)

        embed = discord.Embed(title="チャンネル登録", description="登録完了しました。", color=0x27ae60)
        logger.info('チャンネル登録 成功： 登録完了')
        await ctx.send(embed=embed)

    def validate(self, discord_id, is_record):

        # discord_id
        channel = self.bot.get_channel(discord_id)
        if channel is None:
            logger.info('ボイスチャンネル取得失敗')
            return False

        if channel.type.value != self.CHANNEL_TYPE_VOICE:
            logger.info(f'ボイスチャンネル取得失敗 channel_type: {channel.type.value}')
            return False

        if self.voice_channel_service.find_by_discord_id(discord_id):
            logger.info(f'ボイスチャンネル登録済み discord_id: {discord_id}')
            return False

        # is_record
        if re.compile(r'^(0|1)$').search(str(is_record)) is None:
            logger.info(f'validate error is_record value: {is_record}')
            return False

        return True

    def save_voice_channel(self, discord_id, is_record, created_at):
        self.voice_channel_service.save(discord_id, is_record, created_at)

    @add_voice_channel.error
    async def on_add_voice_channel_error(self, ctx: commands.Context, error):
        embed = discord.Embed(title="チャンネル登録", description="エラーが発生しました。", color=0xc0392b)
        if isinstance(error, BadArgument):
            embed.add_field(name='内容', value='引数はいずれも整数です', inline=False)
        if isinstance(error, MissingRequiredArgument):
            embed.add_field(name='内容', value='引数は2つ必要です', inline=False)

        if isinstance(error, commands.errors.MissingPermissions):  # エラーの内容を判別
            embed.add_field(name='内容', value='権限がありません。', inline=False)
        if isinstance(error, TooManyArguments):
            embed.add_field(name='内容', value='必要な引数は2つのみです', inline=False)

        return await ctx.send(embed=embed)

    @property
    def config(self):
        return __import__('setting')


def setup(bot):
    bot.add_cog(AddVoiceChannel(bot))
