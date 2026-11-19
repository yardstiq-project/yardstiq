from qall.core.provider import login_provider, logout_provider

def login_provider_ys(provider_name: str, **kwargs) -> bool:
    lg = login_provider(provider_name, **kwargs)

    return lg

def logout_provider_ys() -> str:
    return logout_provider()
