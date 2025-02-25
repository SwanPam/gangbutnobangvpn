import asyncio
import asyncpg
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncAttrs, AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import CheckConstraint, ForeignKey, Numeric, String, Boolean, Date, Integer, TIMESTAMP, Text

DB_USER = "postgres"
DB_PASSWORD = "12345"
DB_HOST = "localhost"
DB_NAME = "gangbutnobangvpn"
DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"


engine = create_async_engine(DATABASE_URL, echo=True)
async_session = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

class Base(AsyncAttrs, DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"
    user_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(50), nullable=False)
    main_balance: Mapped[float] = mapped_column(Numeric(10,2), default=0.00)
    referral_balance: Mapped[float] = mapped_column(Numeric(10,2), default=0.00)
    referral_code: Mapped[str] = mapped_column(String(20), unique=True)
    status: Mapped[str] = mapped_column(String(20), default='active')
    
    devices = relationship("Device", back_populates="user")
    payments = relationship("Payment", back_populates="user")

class VPNKey(Base):
    __tablename__ = "vpn_keys"
    key_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    key: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(20), default='active')
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.now())
    deleted_at: Mapped[datetime] = mapped_column(TIMESTAMP)
    
    # Add back reference here
    devices = relationship("Device", back_populates="vpn_key")

class Device(Base):
    __tablename__ = "devices"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id", ondelete="CASCADE"))
    device_name: Mapped[str] = mapped_column(String(100))
    key_id: Mapped[int] = mapped_column(ForeignKey("vpn_keys.key_id", ondelete="SET NULL"))
    status: Mapped[str] = mapped_column(String(20), default='active')
    added_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.now)
    instruction_id: Mapped[int] = mapped_column(Integer, ForeignKey("device_instructions.instruction_id", ondelete="CASCADE"))
    
    user = relationship("User", back_populates="devices")
    instruction = relationship("DeviceInstruction", back_populates="devices")  # Это должна быть двусторонняя связь
    vpn_key = relationship("VPNKey", back_populates="devices", primaryjoin="VPNKey.key_id == Device.key_id")
    
class Notification(Base):
    __tablename__ = "notifications"
    notification_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    message: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.now)
    sent_to_all: Mapped[bool] = mapped_column(Boolean, default=False)
    scheduled_at: Mapped[datetime] = mapped_column(TIMESTAMP)

class DeviceInstruction(Base):
    __tablename__ = "device_instructions"
    instruction_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    device_type: Mapped[str] = mapped_column(String(100))
    instruction_text: Mapped[str] = mapped_column(Text, nullable=False)
    download_link: Mapped[str] = mapped_column(Text)
    
    # Добавляем связь с Device
    devices = relationship("Device", back_populates="instruction")

class Referral(Base):
    __tablename__ = "referrals"
    referrer_id: Mapped[int] = mapped_column(ForeignKey("users.user_id", ondelete="CASCADE"), primary_key=True)
    invitee_id: Mapped[int] = mapped_column(ForeignKey("users.user_id", ondelete="CASCADE"), primary_key=True)
    referrer_bonus_amount: Mapped[float] = mapped_column(Numeric(10,2), default=0.00)
    invitee_bonus_amount: Mapped[float] = mapped_column(Numeric(10,2), default=0.00)
    received: Mapped[bool] = mapped_column(Boolean, default=False)

class PaymentMethod(Base):
    __tablename__ = "payment_methods"
    payment_method_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id", ondelete="CASCADE"))
    method_type: Mapped[str] = mapped_column(
        String(50), CheckConstraint("method_type IN ('card', 'wallet')", name="check_method_type")
    )
    title: Mapped[str] = mapped_column(String(100))
    requisites: Mapped[str] = mapped_column(String(16))
    expiry_date: Mapped[datetime] = mapped_column(Date)

class Payment(Base):
    __tablename__ = "payments"
    payment_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id", ondelete="CASCADE"))
    amount: Mapped[float] = mapped_column(Numeric(10,2), nullable=False)
    status: Mapped[str] = mapped_column(String(20), default='pending', nullable=False)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.now)
    hold_until: Mapped[datetime] = mapped_column(TIMESTAMP)
    type: Mapped[str] = mapped_column(String(50))
    card_title: Mapped[str] = mapped_column(String(100))
    
    user = relationship("User", back_populates="payments")

# Функция для создания таблиц
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
        
if __name__ == "__main__":
    asyncio.run(init_db())
    