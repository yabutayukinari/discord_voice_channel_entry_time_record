from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declarative_base
from loguru import logger

from sqlalchemy_views import CreateView


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


# View追加 TODO: View作成は別ファイルに分離したい。
insp = inspect(engine)
if not insp.has_table("members_date_total_enter_seconds"):
    view = Table('members_date_total_enter_seconds', MetaData())
    definition = text("select member_id, date, sum(channel_enter_seconds) from time_records group by member_id, date")
    create_view = CreateView(view, definition)
    print(str(create_view.compile()).strip())
    engine.execute(create_view)
