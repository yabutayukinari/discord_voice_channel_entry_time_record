from src.settings.setting import *
from sqlalchemy import *


class VoiceStateRecords(Base):
    """
    voice_state_records テーブル定義
    """
    id = Column(Integer, primary_key=True)
    member_id = Column(Integer, nullable=False)
    voice_channel_id = Column(Integer, nullable=False)
    # 1: 入室 2: 退出
    status = Column(Integer, nullable=False)
    created_at = Column(DATETIME, nullable=False)
    __tablename__ = 'voice_state_records'


# 各modelに記載。共通化できるか調査中
Base.metadata.create_all(bind=engine)
