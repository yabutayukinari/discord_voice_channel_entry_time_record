#!/var/bot/type77_test/current/venv/bin/python
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
