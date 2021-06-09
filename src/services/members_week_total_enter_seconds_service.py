from settings.setting import session
from sqlalchemy.sql import text


class MembersWeekTotalEnterSecondsService:

    def find_latest(self, member_id):
        """
        最新データを取得
        """
        sql = text("SELECT * FROM members_week_total_enter_seconds WHERE member_id = :member_id ORDER By week DESC LIMIT 1")

        results = session.execute(sql, {'member_id': str(member_id)}).one()
        return results
