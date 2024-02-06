from typing import Optional, List
from datetime import datetime
from sqlalchemy import Text, ForeignKey, Column, Table
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.pool import NullPool


class Base(DeclarativeBase):
    pass


story_x_locations = Table(
    'story_x_locations',
    Base.metadata,
    Column('story_id', ForeignKey('story.id'), primary_key=True),
    Column('location_id', ForeignKey('location.id'), primary_key=True),
)

story_x_characters = Table(
    'story_x_characters',
    Base.metadata,
    Column('story_id', ForeignKey('story.id'), primary_key=True),
    Column('character_id', ForeignKey('character.id'), primary_key=True),
)


class UserDb(Base):
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(primary_key=True)
    google_id: Mapped[str] = mapped_column(Text, nullable=False)


class SessionDb(Base):
    __tablename__ = 'session'

    id: Mapped[int] = mapped_column(primary_key=True)
    expiration: Mapped[datetime] = mapped_column(nullable=True)
    story_id: Mapped[int] = mapped_column(
        ForeignKey('story.id'), nullable=True)
    current_character_id: Mapped[int] = mapped_column(
        ForeignKey('character.id'), nullable=True)


class StoryDb(Base):
    __tablename__ = 'story'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(Text,)
    setting: Mapped[str] = mapped_column(Text, nullable=True)
    blurb: Mapped[str] = mapped_column(Text, nullable=True)
    is_published: Mapped[bool]
    starting_location_id: Mapped[int] = mapped_column(
        ForeignKey('location.id'), nullable=True)

    starting_location: Mapped['LocationDb'] = relationship(
        lazy='raise', foreign_keys=[starting_location_id])
    locations: Mapped[List['LocationDb']] = relationship(
        back_populates='story', lazy='raise', cascade='all, delete', secondary=story_x_locations)
    characters: Mapped[List['CharacterDb']] = relationship(
        back_populates='story', lazy='raise', cascade='all, delete', secondary=story_x_characters)


class LocationDb(Base):
    __tablename__ = 'location'

    id: Mapped[int] = mapped_column(primary_key=True)
    story_id: Mapped[int] = mapped_column(
        ForeignKey('story.id'), nullable=True)
    name: Mapped[str] = mapped_column(Text,)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    starting_character_id: Mapped[int] = mapped_column(
        ForeignKey('character.id'), nullable=True)

    starting_character: Mapped['CharacterDb'] = relationship(
        lazy='raise', foreign_keys=[starting_character_id])
    story: Mapped['StoryDb'] = relationship(
        back_populates='locations', lazy='raise', foreign_keys=[story_id])


class CharacterDb(Base):
    __tablename__ = 'character'

    id: Mapped[int] = mapped_column(primary_key=True)
    story_id: Mapped[int] = mapped_column(
        ForeignKey('story.id'), nullable=True)
    location_id: Mapped[int] = mapped_column(
        ForeignKey('location.id'), nullable=True)
    name: Mapped[str] = mapped_column(Text,)
    public_description: Mapped[str] = mapped_column(Text, nullable=True)
    private_description: Mapped[str] = mapped_column(Text, nullable=True)

    location: Mapped['LocationDb'] = relationship(
        lazy='raise', foreign_keys=[location_id])
    story: Mapped['StoryDb'] = relationship(
        back_populates='characters', lazy='raise', foreign_keys=[story_id])


async def init_db(user: str, password: str, url: str, port: str, schema_name: str, for_pytest: Optional[bool] = False):
    if for_pytest:
        # Workaround for pytest issues
        engine = create_async_engine(
            f'mysql+aiomysql://{user}:{password}@{url}:{port}/{schema_name}?charset=utf8mb4', poolclass=NullPool)
    else:
        engine = create_async_engine(
            f'mysql+aiomysql://{user}:{password}@{url}:{port}/{schema_name}?charset=utf8mb4')
    sessionmaker = async_sessionmaker(engine, expire_on_commit=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    return engine, sessionmaker


async def close_db(engine):
    await engine.dispose()
