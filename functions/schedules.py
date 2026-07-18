from mastodon import Mastodon
from schedule import Scheduler

from utils.load_env import TZ
from utils.load_yaml import config

from .functions import first_post_boost_scheduled


def create_scheduler(client: Mastodon) -> Scheduler:
    scheduler = Scheduler()
    for time in config["boost_time"]:
        scheduler.every().day.at(time, tz=TZ).do(
            first_post_boost_scheduled, client=client
        )
    return scheduler
