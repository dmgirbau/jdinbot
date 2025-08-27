from __future__ import annotations
from datetime import datetime
from decimal import Decimal


from sqlalchemy import BigInteger, String, Numeric, ForeignKey, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship




class Base(DeclarativeBase):
pass




class User(Base):
__tablename__ = "users"


id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=False)
username: Mapped[str | None] = mapped_column(String(64), nullable=True)
balance: Mapped[Decimal] = mapped_column(Numeric(18, 2), default=0, nullable=False)
created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)


outgoing: Mapped[list["Transaction"]] = relationship(
back_populates="sender", foreign_keys="Transaction.sender_id"
)
incoming: Mapped[list["Transaction"]] = relationship(
back_populates="receiver", foreign_keys="Transaction.receiver_id"
)
