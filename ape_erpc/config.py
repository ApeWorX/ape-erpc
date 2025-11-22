from typing import Optional

from ape.api import PluginConfig
from pydantic import HttpUrl  # noqa: TC002
from pydantic_settings import SettingsConfigDict


class ErpcConfig(PluginConfig):
    host: Optional[HttpUrl] = None
    secret: Optional[str] = None

    model_config = SettingsConfigDict(env_prefix="APE_ERPC_")
