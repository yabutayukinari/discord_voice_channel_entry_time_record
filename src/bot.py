import json
import sys
import traceback
from collections import deque

import discord
from discord.ext import commands
from loguru import logger

import config

description = """

discord_voice_channel_entry_time_record BOT
"""

initial_extensions = (
    'cogs.time_record',
    'cogs.add_member',
    'cogs.add_voice_channel'
)


def _prefix_callable(bot, msg):
    """
    prefix
    :param bot:
    :param msg:
    :return:
    """
    user_id = bot.user.id

    base = [f'<@!{user_id}> ', f'<@{user_id}> ']
    base.append('!')

    return base


class MyBot(commands.AutoShardedBot):
    def __init__(self):
        # Bot基本情報セット？
        allowed_mentions = discord.AllowedMentions(roles=False, everyone=False, users=True)
        super().__init__(command_prefix=_prefix_callable, description=description,
                         pm_help=None, help_attrs=dict(hidden=True),
                         fetch_offline_members=False, heartbeat_timeout=150.0,
                         allowed_mentions=allowed_mentions)

        #
        self.client_id = config.client_id

        self._prev_events = deque(maxlen=10)
        # cog load
        for extension in initial_extensions:
            try:
                self.load_extension(extension)
            except Exception as e:
                print(f'Failed to load extension {extension}.', file=sys.stderr)
                traceback.print_exc()

    def run(self):
        """

        :return:
        """
        try:
            super().run(config.token, reconnect=True)
        finally:
            for data in self._prev_events:
                try:
                    x = json.dumps(data, ensure_ascii=True, indent=4)
                except Exception as e:
                    logger.error(f'{data}')
                else:
                    logger.error(f'{x}')


    @property
    def config(self):
        return __import__('settings')
