from setting import *

from sqlalchemy import *


class Users(Base):
    """
    users テーブル定義
    """
    id = Column(Integer, primary_key=True)
    discord_user_id = Column(Integer, nullable=False)
    created_at = Column(DATETIME, nullable=False)
    __tablename__ = 'users'


# 各modelに記載。共通化できるか調査中
Base.metadata.create_all(bind=engine)
