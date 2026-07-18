from datetime import datetime

from mastodon import Mastodon
from mastodon.return_types import Account, Status

from utils.load_env import MAX_BOOST_DAYS, MAX_FOLLOWERS


def check_public_post(status: Status) -> bool:
    return status.visibility == "public" or status.visibility == "unlisted"


def check_first_post(client: Mastodon, status: Status) -> bool:
    if status.account.statuses_count == 1:
        return True
    statuses_before = client.account_statuses(
        status.account, exclude_reblogs=True, exclude_replies=True, max_id=status
    )
    statuses_before = list(
        filter(
            check_public_post,
            statuses_before,
        )
    )
    return len(statuses_before) == 0


def check_beginner(account: Account) -> bool:
    return account.followers_count <= MAX_FOLLOWERS


def first_post_boost(client: Mastodon, status: Status) -> None:
    if check_first_post(client, status) and check_beginner(status.account):
        client.status_reblog(status)


def first_post_boost_scheduled(client: Mastodon) -> None:
    boost_started = datetime.now()
    since = boost_started - MAX_BOOST_DAYS
    while True:
        tl = client.timeline_local(limit=40, min_id=since)
        for status in tl:
            first_post_boost(client, status)
        if tl[0].created_at >= boost_started or len(tl) < 40:
            break
        since = tl[0].created_at
