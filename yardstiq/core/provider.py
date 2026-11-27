from qall.core.provider import login_provider, logout_provider


def login_provider_ys(provider_name: str, **kwargs) -> bool:
    log = login_provider(provider_name, **kwargs)
    return log


def logout_provider_ys() -> str:
    return logout_provider()
