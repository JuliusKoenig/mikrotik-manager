
from celery.utils.log import get_task_logger

from mikrotik_manager.settings import settings
from mikrotik_manager.worker import celery_app

logger = get_task_logger(__name__)


@celery_app.task(name="test", max_retries=3)
def test(str_attr: str = "qwerty") -> None:
    logger.debug(f"Test task called with str_attr={str_attr} for '{settings.branding_title}'")
