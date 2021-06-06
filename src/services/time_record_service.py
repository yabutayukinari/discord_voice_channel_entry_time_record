from models.time_records import *
from settings.setting import session


class TimeRecordService:

    def save(self, member_id, voice_channel_id, start_time, end_time, date, channel_enter_seconds, created_at):
        time_records = TimeRecords()
        time_records.member_id = member_id
        time_records.voice_channel_id = voice_channel_id
        time_records.start_time = start_time
        time_records.end_time = end_time
        time_records.date = date
        time_records.channel_enter_seconds = channel_enter_seconds
        time_records.created_at = created_at
        session.add(time_records)
        session.commit()
        return time_records








