class Transaction(Base):
__tablename__ = "transactions"


id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
sender_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
receiver_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
amount: Mapped[Decimal] = mapped_column(Numeric(18, 2), nullable=False)
created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)


sender: Mapped[User] = relationship(back_populates="outgoing", foreign_keys=[sender_id])
receiver: Mapped[User] = relationship(back_populates="incoming", foreign_keys=[receiver_id])