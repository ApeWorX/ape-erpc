from ape.api import PluginConfig
from pydantic import HttpUrl  # noqa: TC002
from pydantic_settings import SettingsConfigDict


class ErpcConfig(PluginConfig):
    host: HttpUrl | None = None
    secret: str | None = None

    model_config = SettingsConfigDict(env_prefix="APE_ERPC_")
