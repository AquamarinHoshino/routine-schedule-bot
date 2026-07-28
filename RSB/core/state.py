from datetime import time, timezone, timedelta
import logging
import RSB.config as io


log = logging.getLogger(__name__)

BOT_TOKEN = io.BOT_TOKEN
USER_ID = io.USER_ID
CATEGORIES = io.load_categories()


SMILE_DICT = {
    True: "✅",
    False: "❌"
}


def _get_times() -> tuple:
    settings = io.load_settings()
    return (settings.get("timezone"), settings.get("times"))

TZ, TIMES = _get_times()

def set_times(tz=None, times=None) -> None:
    global TZ, TIMES
    tz = TZ if tz == None else tz
    times = TIMES if times == None else times

    log.info(f"received new time settings, old ({TZ, TIMES}), new ({tz, times})")

    TZ = tz
    TIMES = times

    io.save_settings(tz, times)

def get_schedule_times() -> list[time]:
    global TZ, TIMES
    return [time(i[0], i[1], tzinfo=timezone(timedelta(hours=TZ))) for i in TIMES] 


RESOURCES_COMPLETE = "complete.txt"
RESOURCES_NOT_COMPLETE = "not_complete.txt"
RESOURCES_COMPLETE_N = "complete_n.txt"
RESOURCES_NOT_COMPLETE_N = "not_complete_n.txt"
RESOURCES_REMIND = "remind.txt"