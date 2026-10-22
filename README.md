# ForumBot

A minimal IRC bot that relays messages written to a local file into an IRC channel.

## Behavior

Upon start, the bot will connect to the IRC server irc.inthemansion.com join the #forum-feed channel.
Then it'll periodically check for updates on the forums and send alerts to the channel.

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
