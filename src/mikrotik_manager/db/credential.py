from typing import TYPE_CHECKING

from sqlalchemy import Column, Integer, VARCHAR
from sqlalchemy.orm import relationship

from mikrotik_manager.db.base import Base

if TYPE_CHECKING:
    from mikrotik_manager.db.mikrotik_device import MikrotikDevice


class Credential(Base):
    __tablename__ = "credential"
    __str_columns__ = ["id", "name"]

    id: int = Column(Integer(),
                     primary_key=True,
                     autoincrement=True,
                     name="credential_id")
    name: str = Column(VARCHAR(255),
                       unique=True,
                       nullable=False,
                       name="credential_name")
    mikrotik_device: list["MikrotikDevice"] = relationship("MikrotikDevice",
                                                           foreign_keys="MikrotikDevice.credential_id",
                                                           primaryjoin="Credential.id == MikrotikDevice.credential_id")
    username: str = Column(VARCHAR(255),
                           nullable=False,
                           name="credential_username")
    password: str = Column(VARCHAR(255),
                           nullable=False,
                           name="credential_password")  # ToDo: store device password encrypted
