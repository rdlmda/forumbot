from pathlib import Path
from sopel import plugin

QUEUE_FILE = Path("/tmp/message_queue.txt")
CHANNEL = "#bots2"

@plugin.interval(5)
def check_for_notice(bot):
    if not QUEUE_FILE.exists():
        return

    message = QUEUE_FILE.read_text().strip()
    if message:
        QUEUE_FILE.write_text("")
        bot.say(message, CHANNEL)
