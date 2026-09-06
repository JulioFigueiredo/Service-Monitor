import enum
import uuid

from sqlalchemy import Boolean, Enum, Integer, String, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin


class MonitorType(enum.StrEnum):
    HTTP = "HTTP"
    TCP = "TCP"


class Monitor(Base, TimestampMixin):
    __tablename__ = "monitors"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True,
    )
    user_id: Mapped[uuid.UUID | None] = mapped_column(
        Uuid(as_uuid=True),
        nullable=True,
        index=True,
    )
    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True,
    )
    url: Mapped[str] = mapped_column(
        String(2048),
        nullable=False,
    )
    type: Mapped[MonitorType] = mapped_column(
        Enum(MonitorType, name="monitor_type_enum", native_enum=False),
        default=MonitorType.HTTP,
        nullable=False,
    )
    interval: Mapped[int] = mapped_column(
        Integer,
        default=60,
        nullable=False,
    )
    timeout: Mapped[int] = mapped_column(
        Integer,
        default=5,
        nullable=False,
    )
    expected_status: Mapped[int] = mapped_column(
        Integer,
        default=200,
        nullable=False,
    )
    enabled: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    def __repr__(self) -> str:
        """Return a string representation of the Monitor instance for debugging and logging."""
        return f"<Monitor {self.name} ({self.url}) - {self.type}>"
