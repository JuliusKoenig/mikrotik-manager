from nicegui import ui
from nicegui.client import Client
from fastapi import Request

from mikrotik_manager.settings import settings

from mikrotik_manager.ui.base_layout import BaseLayout

layout = BaseLayout()

# PRIMARY_COLOR = "rgb(144, 164, 174)"
VERTICAL_HEIGHT = "h-[calc(100vh-6.3rem)]"


@layout.section(name="header")
class Header(ui.header):
    def __init__(self, client: Client):
        super().__init__()

        self.props("elevated")
        self.classes("bg-blue-grey-8")

        # ui.colors(primary=PRIMARY_COLOR)
        # ui.add_sass(Path(__file__).parent.parent / "style.sass")

        with self:
            self.header_row = ui.row(align_items="center", wrap=False)
            self.header_row.classes("w-full p-0")

        with self.header_row:
            self.header_left_section = ui.row(align_items="center")
            ui.space()
            self.header_middle_section = ui.row(align_items="center")
            ui.space()
            self.header_right_section = ui.row(align_items="center")

        with self.header_left_section:
            self.graphs_page_button = ui.button(icon="timeline",
                                                color="blue-grey-6" if client.page.path == "/graphs" else "primary")
            self.graphs_page_button.props("dense unelevated")
            self.graphs_page_button.style("margin-right: -10px")
            self.graphs_page_button.tooltip("Diagrammansicht")
            self.graphs_page_button.on_click(
                lambda: None if client.page.path == "/graphs" else ui.navigate.to(target="/graphs"))

            self.measurements_page_button = ui.button(icon="sort",
                                                      color="blue-grey-6" if client.page.path == "/measurements" else "primary")
            self.measurements_page_button.props("dense unelevated")
            self.measurements_page_button.style("margin-right: -10px")
            self.measurements_page_button.tooltip("Messdatenansicht")
            self.measurements_page_button.on_click(
                lambda: None if client.page.path == "/measurements" else ui.navigate.to(target="/measurements"))

            self.files_page_button = ui.button(icon="file_copy",
                                               color="blue-grey-6" if client.page.path == "/files" else "primary")
            self.files_page_button.props("dense unelevated")
            self.files_page_button.style("margin-right: -10px")
            self.files_page_button.tooltip("Dateiansicht")
            self.files_page_button.on_click(
                lambda: None if client.page.path == "/files" else ui.navigate.to(target="/files"))

        with self.header_middle_section:
            self.title = ui.label(settings.branding_title)
            self.title.classes("text-2xl font-bold")




@layout.section()
async def footer(request: Request, client: Client):
    print()
