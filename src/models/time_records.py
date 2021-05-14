from src.settings.setting import *
from sqlalchemy import *


class TimeRecords(Base):
    """
    time_records テーブル定義
    """
    id = Column(Integer, primary_key=True)
    member_id = Column(Integer, nullable=False)
    voice_channel_id = Column(Integer, nullable=False)
    date = Column(Date, nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    # second(秒数) で登録
    channel_enter_seconds = Column(Integer, nullable=False)
    created_at = Column(DATETIME, nullable=False)
    __tablename__ = 'time_records'


# 各modelに記載。共通化できるか調査中
Base.metadata.create_all(bind=engine)
