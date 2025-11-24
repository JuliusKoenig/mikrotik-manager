from celery import Celery

from mikrotik_manager import __name__ as __module_name__
from mikrotik_manager.settings import settings


def get_broker_url():
    broker_url = "pyamqp://"
    if settings.broker_username is not None and settings.broker_password is not None:
        broker_url += f"{settings.broker_username}:{settings.broker_password}@"
    broker_url += f"{settings.broker_host}:{settings.broker_port}//"
    return broker_url


celery_app = Celery(__module_name__,
                    include=[f"{__module_name__}.tasks"],
                    task_cls=f"{__module_name__}.tasks.base:BaseTask")
celery_app.conf.update(broker_url=get_broker_url(),
                       result_backend="rpc://",
                       # beat_scheduler="sqlalchemy_celery_beat.schedulers:DatabaseScheduler",
                       # beat_dburi=get_db_url(),
                       task_serializer="json",
                       result_serializer="json",
                       accept_content=["json"],
                       timezone="Europe/Berlin",
                       enable_utc=True)


def run():
    """
    Run the Celery worker.

    :return: None
    """

    celery_app.worker_main(["worker", "--loglevel=debug"])


if __name__ == "__main__":
    # Run the worker if this script is executed directly
    run()
