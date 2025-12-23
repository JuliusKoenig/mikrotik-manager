from nicegui import ui
from nicegui.client import Client


class Footer(ui.footer):
    def __init__(self, client: Client):
        super().__init__()
