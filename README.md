# ForumBot

A minimal IRC bot that relays messages written to a local file into an IRC channel.

## Behavior

Upon start, the bot will connect to the IRC server irc.inthemansion.com join the #lobby channel.
Then it'll periodically check `/tmp/sopel-alert.txt` and, when the file contains text, sends that text to the channel.

## License

This project is licensed under the GNU Affero General Public License v3.0. See LICENSE for details.
