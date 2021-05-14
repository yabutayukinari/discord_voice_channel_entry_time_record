from src.models.voice_state_records import *
from src.settings.setting import session


class VoiceStateRecordService:

    def find_last_record(self, member_id, voice_channel_id):
        return session.query(VoiceStateRecords).\
        filter(
            VoiceStateRecords.member_id == member_id,
            VoiceStateRecords.voice_channel_id == voice_channel_id,
        ).order_by(desc(VoiceStateRecords.created_at)).first()

    def save(self, member_id, voice_channel_id, status, created_at):
        voice_state_record = VoiceStateRecords()
        voice_state_record.member_id = member_id
        voice_state_record.voice_channel_id = voice_channel_id
        voice_state_record.status = status
        voice_state_record.created_at = created_at
        session.add(voice_state_record)
        session.commit()
        return voice_state_record








