from src.models.voice_state_record import *
from src.settings.setting import session


class VoiceStateRecordService:

    def find_last_record(self, user_id, channel_id):
        return session.query(VoiceStateRecord).\
        filter(
            VoiceStateRecord.user_id == user_id,
            VoiceStateRecord.channel_id == channel_id,
        ).order_by(desc(VoiceStateRecord.created_at)).first()

    def save(self, user_id, channel_id, status, created_at):
        voice_state_record = VoiceStateRecord()
        voice_state_record.user_id = user_id
        voice_state_record.channel_id = channel_id
        voice_state_record.status = status
        voice_state_record.created_at = created_at
        session.add(voice_state_record)
        session.commit()
        return voice_state_record








