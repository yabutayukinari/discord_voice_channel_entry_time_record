from sqlalchemy import *

import models.users
import models.time_records
import models.channels

import setting

from bot import MyBot


def run_bot():
    """

    :return:
    """
    bot = MyBot()
    bot.run()


def main():
    """
    Launches the bot.
    :return:
    """
    run_bot()


if __name__ == '__main__':
    main()
