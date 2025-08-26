from ape import plugins


@plugins.register(plugins.Config)
def config_class():
    from .config import ErpcConfig

    return ErpcConfig


@plugins.register(plugins.ProviderPlugin)
def providers():
    from evmchains import PUBLIC_CHAIN_META

    from .providers import ErpcProvider

    for ecosystem_name, network_info in PUBLIC_CHAIN_META.items():
        for network_name in network_info:
            yield ecosystem_name, network_name, ErpcProvider
