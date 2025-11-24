from wiederverwendbar.uvicorn import UvicornServer

from mikrotik_manager.core_app import __name__ as __core_app_name__, CoreApp as _CoreApp
from mikrotik_manager.settings import settings


class Server(UvicornServer):
    def __init__(self):
        super().__init__(app=f"{__core_app_name__}:{_CoreApp.__name__}",
                         factory=True,
                         settings=settings)
