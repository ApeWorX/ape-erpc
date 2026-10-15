import os
from datetime import datetime, timedelta, timezone

import pytest

from ape_erpc.provider import ErpcProvider

pytestmark = [
    pytest.mark.skipif(
        not os.environ.get("APE_ERPC_HOST"),
        reason="APE_ERPC_HOST not set",
    ),
    pytest.mark.use_network("ethereum:mainnet:erpc"),
]


def test_connection(chain):
    assert isinstance(chain.provider, ErpcProvider)
    assert abs(chain.blocks.head.datetime - datetime.now(timezone.utc)) < timedelta(minutes=1)
