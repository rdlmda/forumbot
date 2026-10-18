import requests
from bs4 import BeautifulSoup
import json
from pathlib import Path
from furl import furl

BASE_URL = "https://forum.inthemansion.com"
STATE_FILE = Path("forum_state.json")

if STATE_FILE.exists():
	state = json.loads(STATE_FILE.read_text())
else:
	state = {}

forum_url = BASE_URL + "/viewforum.php?f=4"
response = requests.get(forum_url, timeout=20)
response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")

for entry in soup.select(".topics li dl"):
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
		print(f'New topic on the forum: "{current["title"]}" ∙ Posted by {current["author"]} on {current["topic_date"]} ∙ {url}')
	elif (
		previous["latest_reply_date"] != latest_reply_date
		or previous["latest_reply_author"] != latest_reply_author
		or previous["replies"] != replies
	):
		print(f'New reply on the topic: "{current["title"]} by {current["author"]}" ∙ {current["replies"]}, {current["views"]} ∙ Reply by {current["latest_reply_author"]} on {current["topic_date"]} ∙ {url}')

	state[url] = current

STATE_FILE.write_text(json.dumps(state, indent=2))
