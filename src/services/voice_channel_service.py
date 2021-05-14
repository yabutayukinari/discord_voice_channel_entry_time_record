from src.models.voice_channels import *
from src.settings.setting import session


class VoiceChannelService:

    def find_is_record(self, channel_id):
        """
        記録対象チャンネルを取得
        :param channel_id:
        :return:
        """
        return session.query(VoiceChannels) \
            .filter(
            VoiceChannels.discord_channel_id == channel_id,
            VoiceChannels.is_record == True) \
            .first()

    def find_by_discord_id(self, discord_id):
        return session.query(VoiceChannels) \
            .filter(VoiceChannels.discord_id == discord_id) \
            .first()
