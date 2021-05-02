from setting import *

from sqlalchemy import *


class TimeRecords(Base):
    """
    time_record テーブル定義
    """
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    channel_id = Column(Integer, nullable=False)
    # 1: 入室 2: 退出 3: その他
    status = Column(Integer, nullable=False)
    created_at = Column(DATETIME, nullable=False)
    __tablename__ = 'time_records'


# 各modelに記載。共通化できるか調査中
Base.metadata.create_all(bind=engine)
