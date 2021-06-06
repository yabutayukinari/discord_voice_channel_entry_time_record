from models.voice_channels import *
from settings.setting import session


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

    def save(self, discord_id, is_record, created_at):
        voice_channels = VoiceChannels()
        voice_channels.discord_id = discord_id
        voice_channels.is_record = is_record
        voice_channels.created_at = created_at
        session.add(voice_channels)
        session.commit()
        return voice_channels
