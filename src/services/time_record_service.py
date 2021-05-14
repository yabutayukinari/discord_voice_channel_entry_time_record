from src.models.time_records import *
from src.settings.setting import session


class TimeRecordService:

    def save(self, member_id, channel_id, start_voice_state_record_id, end_voice_state_record_id, date, total_time, created_at):
        time_records = TimeRecords()
        time_records.member_id = member_id
        time_records.channel_id = channel_id
        time_records.start_voice_state_record_id = start_voice_state_record_id
        time_records.end_voice_state_record_id = end_voice_state_record_id
        time_records.date = date
        time_records.total_time = total_time
        time_records.created_at = created_at
        session.add(time_records)
        session.commit()
        return time_records








