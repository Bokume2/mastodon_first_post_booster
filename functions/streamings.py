from datetime import datetime
from sys import stderr
from time import sleep

from mastodon import Mastodon, StreamListener
from mastodon.return_types import Notification, Status

from utils.load_env import ACCESS_TOKEN, BASE_URL

from .functions import first_post_boost


class Bot(StreamListener):
    def __init__(self, client: Mastodon) -> None:
        super().__init__()
        self.client = client


class LTLBot(Bot):
    def on_update(self, status: Status) -> None:
        first_post_boost(self.client, status)


class HTLBot(Bot):
    def on_notification(self, notification: Notification) -> None:
        if notification.type == "follow":
            self.client.account_follow(notification.account)


def login() -> Mastodon:
    return Mastodon(api_base_url=BASE_URL, access_token=ACCESS_TOKEN)


def ltl_listen(client: Mastodon) -> None:
    lbot = LTLBot(client)
    while True:
        try:
            client.stream_local(lbot)
        except Exception as e:
            print(datetime.now(), file=stderr)
            print(e, file=stderr)
            print(file=stderr)
            sleep(60)


def htl_listen(client: Mastodon) -> None:
    hbot = HTLBot(client)
    while True:
        try:
            client.stream_user(hbot)
        except Exception as e:
            print(datetime.now(), file=stderr)
            print(e, file=stderr)
            print(file=stderr)
            sleep(60)
