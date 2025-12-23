from typing import Optional, TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, Integer, VARCHAR
from sqlalchemy.orm import relationship

from mikrotik_manager.db.base import Base

if TYPE_CHECKING:
    from mikrotik_manager.db.credential import Credential


class MikrotikDevice(Base):
    __tablename__ = "mikrotik_device"
    __str_columns__ = ["id", "name", "hostname", "port"]

    id: int = Column(Integer(),
                     primary_key=True,
                     autoincrement=True,
                     name="mikrotik_device_id")
    credential_id: int = Column(Integer(),
                                ForeignKey("credential.credential_id"),
                                nullable=False,
                                name="mikrotik_device_credential_id")
    credential: Optional["Credential"] = relationship("Credential",
                                                      foreign_keys="Credential.id",
                                                      primaryjoin="MikrotikDevice.credential_id == Credential.id")
    name: str = Column(VARCHAR(255),
                       unique=True,
                       nullable=False,
                       name="mikrotik_device_name")
    hostname: str = Column(VARCHAR(255),
                           nullable=False,
                           name="mikrotik_device_hostname")
    port: int = Column(Integer(),
                       nullable=False,
                       name="mikrotik_device_port")
