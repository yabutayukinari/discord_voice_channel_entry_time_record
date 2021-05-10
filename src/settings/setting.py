from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declarative_base
from loguru import logger
from sqlalchemy import DateTime as SdateTime


# DB接続するためのEngineインスタンス
engine = create_engine('sqlite:///mybot.sqlite3', echo=True)

# DBに対してORM操作するときに利用
# Sessionを通じて操作を行う
session = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine)
)

# 各modelで利用
# classとDBをMapping
Base = declarative_base()

# ログ
logger.remove()
logger.add("logs/log_{time:YYYY-MM-DDTHH:mm}.log", rotation="1 day", retention=30, compression="zip")

