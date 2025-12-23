from typing import Optional, TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, Integer, VARCHAR
from sqlalchemy.orm import relationship

from mikrotik_manager.db.base import Base

if TYPE_CHECKING:
    from mikrotik_manager.db.mikrotik_credential import MikrotikCredential


class MikrotikDevice(Base):
    __tablename__ = "mikrotik_device"
    __str_columns__ = ["id", "name", "hostname", "port"]

    id: int = Column(Integer(),
                     primary_key=True,
                     autoincrement=True,
                     name="mikrotik_device_id")
    mikrotik_credential_id: int = Column(Integer(),
                                         ForeignKey("mikrotik_credential.mikrotik_credential_id"),
                                         nullable=False,
                                         name="mikrotik_device_mikrotik_credential_id")
    mikrotik_credential: Optional["MikrotikCredential"] = relationship("MikrotikCredential",
                                                                       foreign_keys="MikrotikCredential.id",
                                                                       primaryjoin="MikrotikDevice.mikrotik_credential_id == MikrotikCredential.id")
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
