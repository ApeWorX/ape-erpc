from datetime import datetime, timedelta, timezone

from ape_erpc.providers import ErpcProvider


def test_connection(chain):
    assert isinstance(chain.provider, ErpcProvider)
    assert abs(chain.blocks.head.datetime - datetime.now(timezone.utc)) < timedelta(minutes=1)
