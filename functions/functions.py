from mastodon import Mastodon
from mastodon.return_types import Status


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
