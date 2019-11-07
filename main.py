import praw
import time
from bs4 import BeautifulSoup as bs
import requests
import unicodedata
import datetime
from random import randint

with open('config.txt', 'r') as fileobj:
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


def post_to_test(url, subreddits):
    # submits a test post to reddit_api_test
    # title = get_title(url)
    title = "PENULTIMATE TEST"
    for i in range(len(subreddits)):
        sub = subreddits[i]
        subreddit = reddit.subreddit(sub)
        subreddit.submit(
            title=title,
            # selftext='',
            url=url
        )
        if i != len(subreddits) - 1:
            time.sleep(600 + randint(10, 60))
        print(f'Posted article {title}, to {sub}', flush=True)
    # print(url, title, subreddit, flush=True)
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
