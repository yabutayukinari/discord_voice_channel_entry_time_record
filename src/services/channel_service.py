from src.models.channels import *
from src.settings.setting import session


class ChannelService:

    def find_is_record(self, channel_id):
        result = session.query(Channels) \
            .filter(
            Channels.discord_channel_id == channel_id,
            Channels.is_record == True) \
            .first()

        return result
