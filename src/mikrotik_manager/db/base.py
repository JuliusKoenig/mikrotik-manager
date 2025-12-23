from wiederverwendbar.singleton import Singleton
from wiederverwendbar.sqlalchemy import SqlalchemyDb
from wiederverwendbar.sqlalchemy import Base as _Base

from mikrotik_manager.settings import settings


class Db(SqlalchemyDb, metaclass=Singleton):
    ...


def db() -> Db:
    try:
        return Singleton.get_by_type(Db)
    except RuntimeError:
        return Db(settings=settings, init=True)


class Base(_Base, db().Base):
    __abstract__ = True
