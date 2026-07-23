from datetime import datetime, timezone
from time import sleep

from mastodon import Mastodon
from mastodon.return_types import Account, Status

from utils.load_env import MAX_BOOST_DAYS, MAX_FOLLOWERS


def account_initial_setup(client: Mastodon) -> None:
    client.update_notifications_policy(
        for_not_following="accept",
        for_not_followers="accept",
        for_new_accounts="accept",
        for_private_mentions="accept",
        for_limited_accounts="filter",
    )


def check_public_post(status: Status) -> bool:
    return status.visibility == "public"


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


def check_boost_forbiddance(status: Status) -> bool:
    return "ブースト禁止" in status.content


def first_post_boost(client: Mastodon, status: Status) -> None:
    if status.account.id == client.me().id:
        return
    if not (check_first_post(client, status) and check_beginner(status.account)):
        return
    for reply in client.status_context(status).descendants:
        if check_boost_forbiddance(reply) and reply.account.id == status.account.id:
            client.status_unreblog(status)
            return
    client.status_unreblog(status)
    sleep(5)
    client.status_reblog(status)


def first_post_boost_scheduled(client: Mastodon) -> None:
    boost_started = datetime.now(tz=timezone.utc)
    since = boost_started - MAX_BOOST_DAYS
    while True:
        tl = client.timeline_local(limit=40, min_id=since)
        for status in tl:
            first_post_boost(client, status)
        if tl[0].created_at >= boost_started or len(tl) < 40:
            break
        since = tl[0].created_at
