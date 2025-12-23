from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from mikrotik_manager.settings import settings
from mikrotik_manager.ui.app import UiApp


class CoreApp(FastAPI):
    def __init__(self):
        super().__init__(debug=settings.app_debug,
                         root_path=settings.app_root_web_path,
                         docs_url=None,
                         redoc_url=None,
                         openapi_url=None)
        # initialize the UI app
        self.ui_app = UiApp(core_app=self)

        # add root route
        self.add_api_route("/", self.root)

    async def root(self):
        return RedirectResponse(url=settings.app_root_web_path + settings.ui_web_path)
