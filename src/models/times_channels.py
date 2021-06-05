from settings.setting import *
from sqlalchemy import *


class TimesChannels(Base):
    """
    times_channels テーブル定義
    """
    id = Column(Integer, primary_key=True)
    text_channel_id = Column(Integer, nullable=False)
    member_id = Column(Integer, nullable=False, default=True)
    created_at = Column(DATETIME, nullable=False)
    __tablename__ = 'times_channels'


# 各modelに記載。共通化できるか調査中
Base.metadata.create_all(bind=engine)
