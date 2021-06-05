from models.members import *
from settings.setting import session


class MemberService:

    def find_by_discord_id(self, discord_id):
        return session.query(Members) \
            .filter(
            Members.discord_id == discord_id) \
            .first()