from datetime import datetime, timedelta, timezone

import discord
from discord.ext import commands

import config
from services.member_service import *
from services.time_record_service import *
from services.times_channel_service import *
from services.voice_channel_service import *
from services.voice_state_record_service import *
from services.members_date_total_enter_seconds_service import *

TOKEN = config.token


class TimeRecord(commands.Cog):
    JST = timezone(timedelta(hours=+9), 'JST')

    def __init__(self, bot):
        self.bot = bot
        self.member_service = MemberService()
        self.voice_channel_service = VoiceChannelService()
        self.voice_state_record_service = VoiceStateRecordService()
        self.times_channel_service = TimesChannelService()
        self.time_record_service = TimeRecordService()
        self.members_date_total_enter_seconds_service = MembersDateTotalEnterSecondsService()
        self.TIME_RECORD_STATUS_IN = 1
        self.TIME_RECORD_STATUS_OUT = 2
        self.RECORD_ON = True
        self.RECORD_OFF = False

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        """
        入退室
        :param member:
        :param before:
        :param after:
        :return:
        """
        if member.bot:
            logger.info(f'{member.name} : BOTは記録しません')
            return

        # 現在日時
        now = datetime.now(self.JST)

        # ボイスチャンネル入室
        if before.channel is None and after.channel is not None:
            await self.save_voice_state_record(
                member.id,
                after.channel.id,
                after.channel.name,
                self.TIME_RECORD_STATUS_IN,
                now)
            return

        # ボイスチャンネル退室
        if before.channel is not None and after.channel is None:
            await self.save_voice_state_record(
                member.id,
                before.channel.id,
                before.channel.name,
                self.TIME_RECORD_STATUS_OUT,
                now)
            return

        # チャンネル内アクション (ミュートなど)
        if before.channel.id == after.channel.id:
            # 2021/05/11現在 記録しない
            logger.info(f'チャンネル内アクション')
            return

        # チャンネル移動
        if before.channel.id != after.channel.id:
            # 退室
            await self.save_voice_state_record(
                member.id,
                before.channel.id,
                before.channel.name,
                self.TIME_RECORD_STATUS_OUT,
                now
            )

            # 入室
            await self.save_voice_state_record(
                member.id,
                after.channel.id,
                after.channel.name,
                self.TIME_RECORD_STATUS_IN,
                now)
            return

    async def save_voice_state_record(self, discord_member_id, discord_channel_id, discord_channel_name, status, now):
        """
        入退室
        :param discord_member_id:
        :param discord_channel_id:
        :param discord_channel_name:
        :param status:
        :param now:
        :return:
        """
        member = self.find_member(discord_member_id)
        # TODO: 未登録メンバーの通知チャンネルの考慮が必要
        if member is None:
            logger.error(
                f'不明なメンバーの入室を確認 '
                f'discord_member_id:{discord_member_id} '
                f'discord_channel_id:{discord_channel_id} '
            )
            return

        # TODO: timesがない場合を考慮が必要
        times_channel_discord_id = self.find_times_channel_discord_id_by_member_id(member.id)

        # メンバーが記録なしの場合
        if member.is_record is False:
            logger.info(
                f'記録不要メンバー '
                f'discord_member_id:{discord_member_id} '
                f'discord_channel_id:{discord_channel_id} '
            )
            await self.send_message(
                times_channel_discord_id,
                discord_channel_name,
                status,
                self.RECORD_OFF,
                now
            )
            return

        voice_channel = self.find_voice_channel_by_discord_id(discord_channel_id)

        # 未登録ボイスチャンネルの場合
        if voice_channel is None:
            logger.info(
                f'未登録ボイスチャンネル '
                f'discord_member_id:{discord_member_id} '
                f'discord_channel_id:{discord_channel_id} '
                )
            await self.send_message(
                times_channel_discord_id,
                discord_channel_name,
                status,
                self.RECORD_OFF,
                now
            )
            return

        # ボイスチャンネルが記録無の場合
        if voice_channel.is_record is False:
            logger.info(
                f'記録不要チャンネル '
                f'discord_member_id:{discord_member_id} '
                f'discord_channel_id:{discord_channel_id} '
                )
            await self.send_message(
                times_channel_discord_id,
                discord_channel_name,
                status,
                self.RECORD_OFF,
                now
            )
            return

        result = self.voice_state_record_service.save(member.id, voice_channel.id, status, now)
        logger.info(
            f'記録チャンネル '
            f'member.id:{member.id} '
            f'voice_channel.id:{voice_channel.id} '
            f'status:{status} '
            f'created_at:{now} '
        )
        # メッセージ送信
        await self.send_message(
            times_channel_discord_id,
            discord_channel_name,
            status,
            self.RECORD_ON,
            now
        )

        # この処理の中で計測する意味はないので、別途分けたい
        if status == self.TIME_RECORD_STATUS_OUT:
            # 時間計算
            start_voice_state_record = self.find_start_voice_state_record(member.id, voice_channel.id, result.id)
            if start_voice_state_record is None or start_voice_state_record.status != self.TIME_RECORD_STATUS_IN:
                logger.error(f"入室記録がありません。 ユーザー:{member.id} チャンネル:{voice_channel.id}")
                return

            start_day = start_voice_state_record.created_at.strftime("%d")
            end_day = now.strftime("%d")
            if start_day != end_day:
                # 入室時と退出時に日付をまたいだ場合、time_recordは１日毎に記録したいので2レコード登録する
                date_str = start_voice_state_record.created_at.strftime("%Y/%m/%d") + ' 23:59:59'
                date_dt = datetime.strptime(date_str, '%Y/%m/%d %H:%M:%S')
                total_time = date_dt - start_voice_state_record.created_at
                self.save_time_record(member.id,
                                      voice_channel.id,
                                      start_voice_state_record.created_at.time(),
                                      date_dt.time(),
                                      start_voice_state_record.created_at,
                                      total_time,
                                      now)

                date_str = now.strftime("%Y/%m/%d") + ' 00:00:00'
                date_dt = datetime.strptime(date_str, '%Y/%m/%d %H:%M:%S')
                total_time = result.created_at - date_dt
                self.save_time_record(member.id,
                                      voice_channel.id,
                                      date_dt.time(),
                                      now.time(),
                                      now,
                                      total_time,
                                      now)

            else:
                total_time = result.created_at - start_voice_state_record.created_at
                self.save_time_record(member.id,
                                      voice_channel.id,
                                      start_voice_state_record.created_at.time(),
                                      now.time(),
                                      now,
                                      total_time,
                                      now)
        return

    async def send_message(self, send_channel_id, channel_name, status, is_record, now):
        send_channel = self.bot.get_channel(send_channel_id)

        if status == self.TIME_RECORD_STATUS_IN:
            status_value = "入室"
        else:
            status_value = "退出"
        embed = discord.Embed(title=f"{status_value}", color=0x00FFFF)

        if is_record:
            is_record_value = "記録有"
        else:
            is_record_value = "記録無"
        embed.add_field(name="記録種別", value=is_record_value, inline=False)

        embed.add_field(name='チャンネル名', value=channel_name, inline=False)
        embed.add_field(name="現在時刻", value=f"{now.strftime('%Y/%m/%d %H:%M:%S')}", inline=False)

        await send_channel.send(embed=embed)

    def find_voice_channel_by_discord_id(self, discord_id):
        return self.voice_channel_service.find_by_discord_id(discord_id)

    def find_member_by_discord_id(self, discord_id):
        return self.member_service.find_by_discord_id(discord_id)

    def find_member(self, discord_member_id):
        return self.member_service.find_by_discord_id(discord_member_id)

    def find_times_channel_discord_id_by_member_id(self, member_id):
        result = self.times_channel_service.find_discord_id_by_member_id(member_id)
        return result[0]

    def save_time_record(self,
                         member_id,
                         channel_id,
                         start_time,
                         end_time,
                         date,
                         total_time,
                         now):
        """
        入室時間 登録
        :param member_id:
        :param channel_id:
        :param start_time:
        :param end_time:
        :param date:
        :param total_time:
        :param now:
        :return:
        """
        self.time_record_service.save(member_id,
                                      channel_id,
                                      start_time,
                                      end_time,
                                      date,
                                      total_time.seconds,
                                      now)

    def find_start_voice_state_record(self, member_id, channel_id, end_voice_state_record_id):
        return self.voice_state_record_service.find_start_voice_state_record(member_id, channel_id, end_voice_state_record_id)

    @commands.command()
    async def get_today(self, ctx):
        """
        今日の学習時間を取得
        TODO:暫定実装
        """
        now = datetime.now(self.JST)
        member = self.member_service.find_by_discord_id(ctx.author.id)
        result = self.members_date_total_enter_seconds_service.find(member.id, now.date())
        h, m, s = self.get_h_m_s(result[2])
        times_channel_discord_id = self.find_times_channel_discord_id_by_member_id(member.id)

        send_channel = self.bot.get_channel(times_channel_discord_id)

        embed = discord.Embed(title=f"学習時間", color=0x00FFFF)

        embed.add_field(name="日付", value=now.date().strftime('%Y/%m/%d'), inline=False)
        embed.add_field(name="学習時間", value=f"{h}:{m}:{s}", inline=False)

        await send_channel.send(embed=embed)

    @property
    def config(self):
        return __import__('setting')

    def get_h_m_s(self, seconds):
        """
        秒数を、時間、分、秒に変換
        TODO: コピっただけなので見直しが必要
        """
        td = timedelta(seconds=seconds)
        m, s = divmod(td.seconds, 60)
        h, m = divmod(m, 60)
        return h, m, s


def setup(bot):
    bot.add_cog(TimeRecord(bot))
