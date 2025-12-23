from nicegui import ui
from nicegui.client import Client
from fastapi import Request

from mikrotik_manager.ui.components.colors import Colors
from mikrotik_manager.ui.components.header import Header
from mikrotik_manager.ui.components.footer import Footer


@ui.page("/dashboard", title="Dashboard")
async def dashboard(request: Request,
                    client: Client):
    colors = Colors(client)
    header = Header(client)

    ui.label("Diese Seite ist noch in Arbeit.").classes("text-red-500")
    ui.label('CONTENT')
    [ui.label(f'Line {i}') for i in range(100)]

    footer = Footer(client)
