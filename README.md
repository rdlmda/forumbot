# ForumBot

A IRC bot that relays messages written to a local file into an IRC channel.

## Behavior

- The bot will join the #forum-feed channel on irc.inthemansion.com
- It'll then periodically check for updates on the forums.
- Upon each new forum topic or each new reply found, it will send an alert to the channel.
- The bot takes no commands and doesn't react to any DM or message in the channel.

## How does it work

- A helper script is ran periodically (ex.: via crontab on the Docker host) fetching forum data.
- The data is parsed via BeautifulSoup, and if any new data is found, saved to a file.
- A Sopel plugin watches this file and send text from it into the channel.

## Dependencies

- Docker
- Python
  - Sopel
  - BeautifulSoup

## Set up

- Clone this repository
- Build the image: `docker build -t rdlmda/forumbot .`
- Start the bot: `docker run --name forumbot --rm -it -v $(pwd)/forum_state.json:/home/forumbot/app/forum_state.json rdlmda/forumbot`
- Run on the host: `while true; do date; docker exec -it forumbot python /home/forumbot/app/fetch.py; sleep 600; done`

## To-do list

- Fetcher should output on Docker logs.
- Publish an image on Docker Hub.

## License

This project is licensed under the GNU Affero General Public License v3.0. See LICENSE for details.
