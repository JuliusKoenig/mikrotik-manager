from typing import TYPE_CHECKING

from sqlalchemy import Column, Integer, VARCHAR
from sqlalchemy.orm import relationship

from mikrotik_manager.db.base import Base

if TYPE_CHECKING:
    from mikrotik_manager.db.mikrotik_device import MikrotikDevice


class MikrotikCredential(Base):
    __tablename__ = "mikrotik_credential"
    __str_columns__ = ["id", "name"]

    id: int = Column(Integer(),
                     primary_key=True,
                     autoincrement=True,
                     name="mikrotik_credential_id")
    name: str = Column(VARCHAR(255),
                       unique=True,
                       nullable=False,
                       name="mikrotik_credential_name")
    mikrotik_device: list["MikrotikDevice"] = relationship("MikrotikDevice",
                                                           foreign_keys="MikrotikDevice.mikrotik_credential_id",
                                                           primaryjoin="MikrotikCredential.id == MikrotikDevice.credential_id")
    username: str = Column(VARCHAR(255),
                           nullable=False,
                           name="mikrotik_credential_username")
    password: str = Column(VARCHAR(255),
                           nullable=False,
                           name="mikrotik_credential_password")  # ToDo: store device password encrypted
