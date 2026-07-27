from datetime import time
from pytz import timezone

import RSB.config as io


BOT_TOKEN = io.BOT_TOKEN
USER_ID = io.USER_ID
CATEGORIES = io.load_categories()
 
SMILE_DICT = {
    True: "✅",
    False: "❌"
}

tz = timezone('Asia/Yekaterinburg')
SCHEDULE_TIMES = [
    time(17, 48, tzinfo=tz),
    time(17, 50, tzinfo=tz),
    time(17, 55, tzinfo=tz)
]

RESOURCES_COMPLETE = "complete.txt"
RESOURCES_NOT_COMPLETE = "not_complete.txt"
RESOURCES_COMPLETE_N = "complete_n.txt"
RESOURCES_NOT_COMPLETE_N = "not_complete_n.txt"
RESOURCES_REMIND = "remind.txt"