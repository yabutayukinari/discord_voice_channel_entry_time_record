from src.models.time_record import *
from src.settings.setting import session


class TimeRecordService:

    def save(self, user_id, channel_id, start_voice_state_record_id, end_voice_state_record_id, total_time, created_at):
        time_record = TimeRecord()
        time_record.user_id = user_id
        time_record.channel_id = channel_id
        time_record.start_voice_state_record_id = start_voice_state_record_id
        time_record.end_voice_state_record_id = end_voice_state_record_id
        time_record.total_time = total_time
        time_record.created_at = created_at
        session.add(time_record)
        session.commit()
        return time_record








