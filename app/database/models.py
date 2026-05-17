from sqlalchemy import BigInteger, String, Integer, UniqueConstraint, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs
from datetime import datetime

engine = create_async_engine(url='sqlite+aiosqlite:///db.sqlite3')
async_session = async_sessionmaker(engine, expire_on_commit=False)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    username: Mapped[str | None] = mapped_column(String(100), nullable=True)
    first_name: Mapped[str | None] = mapped_column(String(100), nullable=True)
    language: Mapped[str] = mapped_column(String(10), default='en')
    total_points: Mapped[int] = mapped_column(Integer, default=0)


class Game(Base):
    __tablename__ = 'games'

    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column(String(50), unique=True)
    team1: Mapped[str] = mapped_column(String(50))
    team2: Mapped[str] = mapped_column(String(50))
    match_date: Mapped[str] = mapped_column(String(20))
    match_time: Mapped[str] = mapped_column(String(20))
    result: Mapped[str | None] = mapped_column(String(20), nullable=True)
    winner: Mapped[str | None] = mapped_column(String(50), nullable=True)


class Prediction(Base):
    __tablename__ = 'predictions'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_tg_id: Mapped[int] = mapped_column(BigInteger)
    game_code: Mapped[str] = mapped_column(String(50))
    selected_team: Mapped[str] = mapped_column(String(50))
    points: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[str] = mapped_column(String(50), default=lambda: datetime.now().isoformat())

    __table_args__ = (
        UniqueConstraint('user_tg_id', 'game_code', name='unique_user_game_prediction'),
    )


async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
