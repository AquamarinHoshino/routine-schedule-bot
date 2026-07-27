import logging

from telegram import Update
from telegram.ext import ContextTypes, ApplicationHandlerStop

from RSB.core.state import USER_ID

log = logging.getLogger(__name__)


async def restrict_access(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id != USER_ID:
        log.info(f"unauthorized access by {user_id} {update.effective_user.link}")
        raise ApplicationHandlerStop