from src.settings.setting import *
from sqlalchemy import *


class TimeRecord(Base):
    """
    time_record テーブル定義
    """
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    channel_id = Column(Integer, nullable=False)
    # 1: 入室 2: 退出 3: その他
    start_voice_state_record_id = Column(Integer, nullable=False)
    end_voice_state_record_id = Column(Integer, nullable=False)
    # second で登録
    total_time = Column(Integer, nullable=False)
    created_at = Column(DATETIME, nullable=False)
    __tablename__ = 'time_record'


# 各modelに記載。共通化できるか調査中
Base.metadata.create_all(bind=engine)
