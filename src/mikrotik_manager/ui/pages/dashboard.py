from nicegui import ui
from nicegui.client import Client
from fastapi import Request

from mikrotik_manager.ui.layout import layout, Header


@layout.page("/dashboard", title="Dashboard")
async def dashboard(request: Request,
                    client: Client,
                    header: Header):
    ui.label("Diese Seite ist noch in Arbeit.").classes("text-red-500")
    ui.label('CONTENT')
    [ui.label(f'Line {i}') for i in range(100)]
