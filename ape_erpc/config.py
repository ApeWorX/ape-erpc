from typing import Optional

from ape.api import PluginConfig
from pydantic import HttpUrl  # noqa: TC002


class ErpcConfig(PluginConfig):
    host: Optional[HttpUrl] = None
