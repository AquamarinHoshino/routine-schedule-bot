import logging
import datetime as dt
import os
import RSB.bot as bot


log = logging.getLogger(__name__)

def setup_logging():
    logger = logging.getLogger()          # root logger
    logger.setLevel(logging.DEBUG)        # минимальный уровень для root

    # --- консоль: только INFO и выше ---
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    console.setFormatter(logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%H:%M:%S"
    ))

    # --- файл: всё включая DEBUG, с ротацией ---
    if not os.path.isdir('logs'):
        os.mkdir('logs')
    from logging.handlers import RotatingFileHandler
    file_h = RotatingFileHandler(
       os.path.join("logs", f"{str(dt.datetime.today()).replace(" ", '_').replace(":", '-')}.log"), maxBytes=5 * 1024 * 1024, backupCount=3, encoding="utf-8"
    )
    file_h.setLevel(logging.DEBUG)
    file_h.setFormatter(logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s (%(filename)s:%(lineno)d): %(message)s"
    ))

    logger.addHandler(console)
    logger.addHandler(file_h)

def main():
    setup_logging()
    bot.main()

if __name__ == '__main__':
    main()