from models.times_channels import *
from models.text_channels import *
from settings.setting import session


class TimesChannelService:

    def find_discord_id_by_member_id(self, member_id):
        return session.query(TextChannels.discord_id) \
            .join(TimesChannels, TimesChannels.text_channel_id == TextChannels.id) \
            .filter(
            TimesChannels.member_id == member_id) \
            .first()
