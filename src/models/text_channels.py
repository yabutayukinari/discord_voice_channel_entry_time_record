from settings.setting import *
from sqlalchemy import *


class TextChannels(Base):
    """
    text_channels テーブル定義
    """
    id = Column(Integer, primary_key=True)
    discord_id = Column(Integer, nullable=False)
    created_at = Column(DATETIME, nullable=False)
    __tablename__ = 'text_channels'


# 各modelに記載。共通化できるか調査中
Base.metadata.create_all(bind=engine)
