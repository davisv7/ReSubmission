import praw
import time
from bs4 import BeautifulSoup as bs
import requests
import unicodedata
import datetime
from random import randint

with open('config.txt', 'r') as fileobj:  # pulls account info out of config file
    client_id, client_secret, user_agent, username, password = [line.strip('\r\n') for line in fileobj.readlines()]

reddit = praw.Reddit(
    client_id=client_id,
    client_secret=client_secret,
    user_agent=user_agent,
    username=username,
    password=password
)


def get_title(url):
    # gets the title of the article from the web
    with requests.get(url) as urlobj:
        soup = bs(urlobj.content, "html.parser")
        title = soup.find("h1", class_="Headings__H1-sc-1ibq1fi-0 PostHeader__Heading-sc-1cg3u6k-4 fXgBJm").text
        title = unicodedata.normalize('NFKD', title).encode('ascii', 'ignore').decode("utf-8")
        return title


def post_to_subs(url, subreddits):
    # submits a link post (url) to all subs in subreddits list
    title = get_title(url)
    for i in range(len(subreddits)):
        sub = subreddits[i]
        try:
            subreddit = reddit.subreddit(sub)
            subreddit.submit(
                title=title,
                url=url
            )
            if i != len(subreddits) - 1:  # we don't want to wait 10 minutes after the last post is complete
                time.sleep(600 + randint(10, 60))
            print(f'Posted article {title}, to {sub}', flush=True)
        except Exception as e:
            print(f'Error posting {title} to {sub}')
            print(e, flush=True)

    print('Posting complete.', flush=True)
    print(f'Please wait until after {get_time(10)} before posting again.', flush=True)


def get_def_subs():
    # gets default subs from file to populate checklist
    with open('subreddits.txt', 'r') as fileobj:
        subs = [(sub.strip('\r\n'), sub) for sub in fileobj.readlines()]
    return subs


def get_time(number):
    # returns an estimate for the time it will take to finish posting
    return (datetime.datetime.now() + datetime.timedelta(minutes=number)).time().strftime('%H:%M:%S.%f')[:-6]
