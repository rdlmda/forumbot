import requests
from bs4 import BeautifulSoup
import json
from pathlib import Path
from furl import furl
from time import sleep

STATE_FILE = Path("forum_state.json")
QUEUE_FILE = Path("/tmp/message_queue.txt")
BASE_URL = "https://forum.inthemansion.com"

if STATE_FILE.exists():
	state = json.loads(STATE_FILE.read_text())
else:
	state = {}

forums = ['4', '5', '7', '8', '12', '13', '14','35', '34', '16', '17', '36', '19', '21', '30', '31', '32', '23', '27', '28', '25']

for i, forum in enumerate(forums):
	print(f"Fetching forum {forum} ({i+1}/{len(forums)})", end="... ")
	forum_url = BASE_URL + '/viewforum.php?f=' + forum
	response = requests.get(forum_url, timeout=20)
	response.raise_for_status()

	soup = BeautifulSoup(response.text, "html.parser")

	entries = soup.select(".topics li dl")
	for entry in entries:
		title = entry.select('.topictitle')[0].get_text()
		url = furl(BASE_URL + entry.select('.topictitle')[0].get('href')[1:]).remove(['sid']).url
		author = entry.select('.topic-poster a')[0].get_text()
		topic_date = entry.select('.topic-poster time')[0].get_text()
		replies = entry.select('.posts')[0].get_text()
		views = entry.select('.views')[0].get_text()
		latest_reply_author = entry.select('.lastpost a')[0].get_text()
		latest_reply_date = entry.select('.lastpost time')[0].get_text()

		current = {
			"title": title,
			"author": author,
			"topic_date": topic_date,
			"replies": replies,
			"views": views,
			"latest_reply_author": latest_reply_author,
			"latest_reply_date": latest_reply_date,
		}

		previous = state.get(url)

		if previous is None:
			message = f'New topic on the forum: "{current["title"]}" ∙ Posted by {current["author"]} on {current["topic_date"]} ∙ {url}'
			QUEUE_FILE.write_text(message)
		elif (
			previous["latest_reply_date"] != latest_reply_date
			or previous["latest_reply_author"] != latest_reply_author
			or previous["replies"] != replies
		):
			message = f'New reply on the topic: "{current["title"]} by {current["author"]}" ∙ {current["replies"]}, {current["views"]} ∙ Reply by {current["latest_reply_author"]} on {current["latest_reply_date"]} ∙ {url}'
			QUEUE_FILE.write_text(message)

		state[url] = current
	STATE_FILE.write_text(json.dumps(state, indent=2))
	print(f"{len(entries)} fetched.")
	sleep(5)
