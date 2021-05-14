from src.settings.setting import *
from sqlalchemy import *


class Members(Base):
    """
    users テーブル定義
    """
    id = Column(Integer, primary_key=True)
    discord_id = Column(Integer, nullable=False)
    is_record = Column(Boolean, nullable=False, default=True)
    created_at = Column(DATETIME, nullable=False)
    __tablename__ = 'members'


# 各modelに記載。共通化できるか調査中
Base.metadata.create_all(bind=engine)
