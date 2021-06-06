from settings.setting import session
from sqlalchemy.sql import text


class MembersDateTotalEnterSecondsService:

    def find(self, member_id, date):
        sql = text("SELECT * FROM members_date_total_enter_seconds WHERE member_id = :member_id AND date = :date")

        results = session.execute(sql, {'member_id': str(member_id), 'date': str(date)}).one()
        return results
