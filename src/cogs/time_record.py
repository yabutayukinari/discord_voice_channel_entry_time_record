from src import config
from discord.ext import commands
from src.services.voice_state_record_service import *
from src.services.channel_service import *
from src.services.time_record_service import *
from datetime import datetime, timedelta, timezone

TOKEN = config.token


class TimeRecord(commands.Cog):
    JST = timezone(timedelta(hours=+9), 'JST')
    TIME_RECORD_STATUS_IN = 1
    TIME_RECORD_STATUS_OUT = 2

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if member.bot:
            print(f'{member.name} : BOTは記録しません')
            return

        # 現在日時
        now = datetime.now(self.JST)

        # VC入室時
        if before.channel is None and after.channel is not None:
            self.update_voice_state(member.id, after.channel.id, self.TIME_RECORD_STATUS_IN, now)
            return

        # VC退室時
        if before.channel is not None and after.channel is None:
            # 入室記録チェック
            time_record_service = VoiceStateRecordService()
            start_voice_state_record = time_record_service.find_last_record(member.id, before.channel.id)
            if start_voice_state_record is None:
                logger.error(f"入室記録がありません。 ユーザー:{member.id} チャンネル:{before.channel.id}")
                return

            end_voice_state_record = self.update_voice_state(member.id, before.channel.id, self.TIME_RECORD_STATUS_OUT, now)

            if end_voice_state_record is None:
                return

            self.save_time_record(start_voice_state_record, end_voice_state_record, now)
            return

        # チャンネル内アクション
        if before.channel.id == after.channel.id:
            logger.info(f'チャンネル内アクション')
            return

        # チャンネル移動
        if before.channel.id != after.channel.id:
            # 入室記録チェック
            time_record_service = VoiceStateRecordService()
            start_voice_state_record = time_record_service.find_last_record(member.id, before.channel.id)
            if start_voice_state_record is None:
                logger.error(f"入室記録がありません。 ユーザー:{member.id} チャンネル:{before.channel.id}")
                return

            end_voice_state_record = self.update_voice_state(
                member.id, before.channel.id, self.TIME_RECORD_STATUS_OUT, now)
            if end_voice_state_record is None:
                return

            self.save_time_record(start_voice_state_record, end_voice_state_record, now)
            # 入室
            self.update_voice_state(member.id, after.channel.id, self.TIME_RECORD_STATUS_IN, now)
            return

    @property
    def config(self):
        return __import__('setting')

    def update_voice_state(self, member_id, channel_id, status, created_at):
        if self.is_record_channel(channel_id) is False:
            logger.info(f'記録不要チャンネル')
            return None

        return self.save_voice_state_record(member_id, channel_id, status, created_at)

    def save_time_record(self, start_voice_state_record, end_voice_state_record, now):
        total_time = end_voice_state_record.created_at - start_voice_state_record.created_at
        time_record_service = TimeRecordService()
        time_record_service.save(start_voice_state_record.user_id, start_voice_state_record.channel_id, start_voice_state_record.id, end_voice_state_record.id, total_time.seconds, now)


    def save_voice_state_record(self, member_id, channel_id, status, created_at):

        voice_state_record_service = VoiceStateRecordService()
        voice_state_record = voice_state_record_service.save(member_id, channel_id, status, created_at)
        logger.info(
            f"ユーザー:{member_id} チャンネル:{channel_id} ステータス:{status} 時刻:{created_at.strftime('%Y/%m/%d %H:%M:%S')}")

        return voice_state_record

    def is_record_channel(self, discord_channel_id):
        channel_service = ChannelService()
        if channel_service.find_is_record(discord_channel_id):
            return true
        else:
            return false


def setup(bot):
    bot.add_cog(TimeRecord(bot))
