from typing import TYPE_CHECKING, cast

from ape.api import UpstreamProvider
from ape_ethereum.provider import Web3Provider
from web3 import HTTPProvider, Web3
from web3.exceptions import ExtraDataLengthError
from web3.gas_strategies.rpc import rpc_gas_price_strategy
from web3.middleware.validation import MAX_EXTRADATA_LENGTH

try:
    from web3.middleware import ExtraDataToPOAMiddleware  # type: ignore
except ImportError:
    from web3.middleware import geth_poa_middleware as ExtraDataToPOAMiddleware  # type: ignore

if TYPE_CHECKING:
    from .config import ErpcConfig


class ErpcProvider(Web3Provider, UpstreamProvider):
    """
    A web3 provider using eRPC caching RPC proxy.

    Docs: https://docs.alchemy.com/alchemy/
    """

    @property
    def config(self) -> "ErpcConfig":
        return cast("ErpcConfig", self.config_manager.get_config("erpc"))

    @property
    def uri(self) -> str:
        if not (host := self.config.host):
            raise ValueError
        return f"{str(host).rstrip('/')}/evm/{self.chain_id}"

    @property
    def http_uri(self) -> str:
        # NOTE: Overriding `Web3Provider.http_uri` implementation
        return self.uri

    @property
    def ws_uri(self):
        # NOTE: Overriding `Web3Provider.http_uri` implementation
        return None

    def connect(self):
        self._web3 = Web3(HTTPProvider(self.uri))
        is_poa = None
        try:
            # Any chain that *began* as PoA needs the middleware for pre-merge blocks
            base = 8453
            optimism = 10
            polygon = 137
            polygon_amoy = 80002

            if self._web3.eth.chain_id in (base, optimism, polygon, polygon_amoy):
                self._web3.middleware_onion.inject(ExtraDataToPOAMiddleware, layer=0)
                is_poa = True

            self._web3.eth.set_gas_price_strategy(rpc_gas_price_strategy)
        except Exception:
            is_poa = None

        if is_poa is None:
            # Check if is PoA but just wasn't as such yet.
            # NOTE: We have to check both earliest and latest
            #   because if the chain was _ever_ PoA, we need
            #   this middleware.
            for option in ("earliest", "latest"):
                try:
                    block = self.web3.eth.get_block(option)  # type: ignore[arg-type]
                except ExtraDataLengthError:
                    is_poa = True
                    break
                else:
                    is_poa = (
                        "proofOfAuthorityData" in block
                        or len(block.get("extraData", "")) > MAX_EXTRADATA_LENGTH
                    )
                    if is_poa:
                        break

            if is_poa and ExtraDataToPOAMiddleware not in self.web3.middleware_onion:
                self.web3.middleware_onion.inject(ExtraDataToPOAMiddleware, layer=0)

    def disconnect(self):
        self._web3 = None
