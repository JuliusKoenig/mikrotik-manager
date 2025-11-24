from wiederverwendbar.typer import Typer
from wiederverwendbar.logger import LoggerSingleton

from mikrotik_manager import __name__ as __module_name__
from mikrotik_manager.settings import settings

logger = LoggerSingleton(name=__module_name__,
                         settings=settings,
                         ignored_loggers_like=["sqlalchemy", "pymysql", "asyncio", "parso", "engineio", "socketio"],
                         init=True)

cli_app = Typer(settings=settings)


@cli_app.command(name="serve", help=f"Start the {settings.branding_title} - server.")
def serve_command() -> None:
    """
    Start the Server.

    :return: None
    """

    import pidfile
    from mikrotik_manager.server import Server

    # print header
    cli_app.console.print(f"Starting {settings.branding_title} - server ...")
    cli_app.console.print(f"[white]{cli_app.title_header}[/white]")

    # ToDo: test DB

    # start server
    if settings.app_pid_file:
        try:
            with pidfile.PIDFile(settings.app_pid_file):
                Server()
        except pidfile.AlreadyRunningError:
            cli_app.console.print(f"[red]Error:[/red] Another instance of {settings.branding_title} is already running.")
    else:
        Server()


@cli_app.command(name="worker", help=f"Start the {settings.branding_title} - worker.")
def worker_command() -> None:
    """
    Start the Worker.

    :return: None
    """

    from mikrotik_manager.worker import run

    # print header
    cli_app.console.print(f"Starting {settings.branding_title} - worker ...")
    cli_app.console.print(f"[white]{cli_app.title_header}[/white]")

    # ToDo: test DB

    # start server
    run()

@cli_app.command(name="init", help=f"Initialize database.")
def init_command() -> None:
    """
    Initialize database.

    :return: None
    """

    from mikrotik_manager.db import db

    # print header
    cli_app.console.print(f"Initializing database ...")
    cli_app.console.print(f"[white]{cli_app.title_header}[/white]")

    # initialize DB
    db().create_all()
