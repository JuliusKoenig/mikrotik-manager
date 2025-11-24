import os
import sys
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, Field, DirectoryPath, ValidationError
from pydantic_settings import BaseSettings
from wiederverwendbar.logger import LoggerSettings
from wiederverwendbar.pydantic import Version
from wiederverwendbar.pydantic.file.yaml import YamlFile
from wiederverwendbar.sqlalchemy import SqlalchemySettings
from wiederverwendbar.uvicorn import UvicornServerSettings
from wiederverwendbar.typer import TyperSettings

from mikrotik_manager import __title__, __description__, __version__, __author__, __author_email__, __license__, \
    __license_url__, __terms_of_service__


# ToDo: move to wiederverwendbar
class CelerySettings(SqlalchemySettings):
    worker_pid_file: Path | None = Field(default=None,
                                         title="Worker PID File",
                                         description="The path to the worker PID file. If None, no PID file is created.")
    worker_uid: str | None = Field(default=None,
                                   title="Worker User",
                                   description="The user to run the worker as. If None, the worker runs as the current user.")
    worker_gid: str | None = Field(default=None,
                                   title="Worker Group",
                                   description="The group to run the worker as. If None, the worker runs as the current group.")
    # ToDo: Beat settings
    # BEAT_LOG_LEVEL=INFO
    # BEAT_LOG_FILE_ENABLED=true
    # BEAT_LOG_FILE=/var/log/celery/beat.log
    # BEAT_PID_FILE=/var/run/celery/beat.pid
    # BEAT_UID=nobody
    # BEAT_GID=nogroup
    broker_host: str = Field(default="localhost",
                             title="Broker Host",
                             description="The host of the AMQ message broker.")
    broker_port: int = Field(default=5672,
                             title="Broker Port",
                             description="The port of the AMQ message broker.")
    broker_username: str | None = Field(default=None,
                                        title="Broker Username",
                                        description="The username to connect to the AMQ message broker.")
    broker_password: str | None = Field(default=None,
                                        title="Broker Password",
                                        description="The password to connect to the AMQ message broker.")


class Settings(CelerySettings, UvicornServerSettings, TyperSettings, LoggerSettings, YamlFile):
    model_config = {
        "case_sensitive": False,
        "file_overwrite": {
            "branding_title": __title__,
            "branding_description": __description__,
            "branding_version": Version(__version__),
            "branding_author": __author__,
            "branding_author_email": __author_email__,
            "branding_license": __license__,
            "branding_license_url": __license_url__,
            "branding_terms_of_service": __terms_of_service__
        },
        "file_save_on_load": "if_not_exist"
    }

    # app
    app_debug: bool = Field(default=False, description="App debug mode.")
    app_root_web_path: str = Field(default="", description="App root web path.")
    app_pid_file: Path | None = Field(default=None, description="App PID file path.")

    # ui
    ui_web_path: str = Field(default="/ui", description="UI web path prefix.")
    ui_default_path: str | None = Field(default="/dashboard", description="Default UI path.")
    ui_viewport: str = Field(default="width=device-width, initial-scale=1", description="Viewport meta tag.")
    ui_favicon: str | Path | None = Field(default=Path("logo.png"), description="Favicon path.")
    ui_dark: bool = Field(default=False, description="Dark mode.")
    ui_language: Literal["ar", "ar-TN", "az-Latn", "bg", "bn", "ca", "cs", "da", "de", "el", "en-GB", "en-US",
    "eo", "es", "et", "eu", "fa", "fa-IR", "fi", "fr", "gn", "he", "hr", "hu", "id", "is", "it", "ja",
    "kk", "km", "ko-KR", "kur-CKB", "lt", "lu", "lv", "ml", "mm", "ms", "my", "nb-NO", "nl", "pl", "pt",
    "pt-BR", "ro", "ru", "sk", "sl", "sm", "sr", "sr-CYR", "sv", "ta", "th", "tr", "ug", "uk", "uz-Cyrl",
    "uz-Latn", "vi", "zh-CN", "zh-TW"] = Field(default="en-US", description="Language.")
    ui_reconnect_timeout: float = Field(default=3.0, description="Reconnect timeout.")
    ui_prod_js: bool = Field(default=False,
                             description="Use production JavaScript.")  # ToDo: set default to True in production
    ui_storage_secret: str = Field(default="test", description="Storage secret.")  # ToDo: make storage_secret required


try:
    settings = Settings.load()
except ValidationError as e:
    print("Settings validation error:", e)
    sys.exit(1)
