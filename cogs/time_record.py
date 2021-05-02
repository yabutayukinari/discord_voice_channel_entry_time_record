import discord
import config
from discord.ext import commands

TOKEN = config.token


class TimeRecord(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if member.bot:
            print(f'{member.name} : BOTは記録しません')
            return

        # VC入室時
        if before.channel is None and after.channel is not None:

            # 記録不要チャンネル TODO: 判定は内部DBで行うようにする。 記録有無の変更はコマンドで行う。
            if '記録不要' in after.channel.name:
                print(f'記録不要チャンネル')
                return

            print(f'VC入室時')
            return

        # VC退室時
        if before.channel is not None and after.channel is None:

            # 記録不要チャンネル
            if '記録不要' in before.channel.name:
                print(f'記録不要チャンネル')
                return

            print(f'VC退室時')
            return

        # チャンネル内アクション
        if before.channel.id == after.channel.id:
            print(f'チャンネル内アクション')
            return


        # チャンネル移動
        if before.channel.id != after.channel.id:
            print(f'チャンネル移動')
            return

    @property
    def config(self):
        return __import__('config')


def setup(bot):
    bot.add_cog(TimeRecord(bot))