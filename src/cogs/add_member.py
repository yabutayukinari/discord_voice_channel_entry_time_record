import discord
from datetime import datetime, timedelta, timezone
from discord.ext import commands
from services.member_service import *
from loguru import logger


class AddMember(commands.Cog):
    JST = timezone(timedelta(hours=+9), 'JST')

    def __init__(self, bot):
        self.bot = bot
        self.member_service = MemberService()

    @commands.command()
    async def add_member(self, ctx, *args):
        """
        メンバー登録
        TODO: 現在はコマンド実行者を登録、 引数にidある場合、idを登録するように変更する。
        :param ctx:
        :param args:
        :return:
        """
        # 現在日時
        now = datetime.now(self.JST)
        # TODO: コマンド利用権限チェック roleで制御 自分意外を追加する場合はチェックが欲しい
        discord_member_id = ctx.author.id
        member = self.member_service.find_by_discord_id(discord_member_id)

        if member:
            embed = discord.Embed(title="メンバー登録", description="すでに登録されています。", color=0xc0392b)
            embed.add_field(name='メンバー名', value=ctx.author.display_name, inline=False)
            embed.add_field(name='登録日', value=member.created_at, inline=False)
            await ctx.send(embed=embed)
            return

        self.save_member(discord_member_id, now)

        embed = discord.Embed(title="メンバー登録", description="登録完了しました。", color=0x27ae60)
        embed.add_field(name='メンバー名', value=ctx.author.display_name, inline=False)

        await ctx.send(embed=embed)

    def save_member(self, discord_member_id, created_at):
        """
        メンバー登録
        :param discord_member_id:
        :param created_at:
        :return:
        """
        self.member_service.save(discord_member_id, created_at)

    @property
    def config(self):
        return __import__('setting')


def setup(bot):
    bot.add_cog(AddMember(bot))
