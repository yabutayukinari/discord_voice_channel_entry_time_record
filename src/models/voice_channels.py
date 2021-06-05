from settings.setting import *
from sqlalchemy import *


class VoiceChannels(Base):
    """
    users テーブル定義
    """
    id = Column(Integer, primary_key=True)
    discord_id = Column(Integer, nullable=False)
    is_record = Column(Boolean, nullable=False)
    created_at = Column(DATETIME, nullable=False)
    __tablename__ = 'voice_channels'


# 各modelに記載。共通化できるか調査中
Base.metadata.create_all(bind=engine)
