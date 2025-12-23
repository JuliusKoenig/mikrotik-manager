from nicegui import ui
from nicegui.client import Client

PRIMARY_COLOR = "rgb(144, 164, 174)"



class Colors(ui.colors):
    def __init__(self, client: Client):
        super().__init__(primary=PRIMARY_COLOR)
