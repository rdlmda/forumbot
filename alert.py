from pathlib import Path
from sopel import plugin

QUEUE = Path("/tmp/sopel-alert.txt")
CHANNEL = "#bots2"

@plugin.interval(5)
def check_for_notice(bot):
    if not QUEUE.exists():
        return

    message = QUEUE.read_text().strip()
    if message:
        QUEUE.write_text("")
        bot.say(message, CHANNEL)
