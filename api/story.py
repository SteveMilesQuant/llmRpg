from pydantic import PrivateAttr
from typing import Optional, Any, List
from sqlalchemy import select
from datamodels import StoryData, StoryResponse
from db import StoryDb, LocationDb, CharacterDb


class Story(StoryResponse):
    _db_obj: Optional[StoryDb] = PrivateAttr()

    def __init__(self, db_obj: Optional[StoryDb] = None, **data):
        super().__init__(**data)
        self._db_obj = db_obj

    async def create(self, session: Optional[Any]):
        if self._db_obj is None and self.id is not None:
            # Get by ID
            self._db_obj = await session.get(StoryDb, [self.id])
            if self._db_obj is None:
                self.id = None
                return

        if self._db_obj is None:
            # If none found, create new
            story_data = self.dict(include=StoryData().dict())
            self._db_obj = StoryDb(**story_data)
            session.add(self._db_obj)
            await session.commit()
            self.id = self._db_obj.id
        else:
            # Otherwise, update attributes from fetched object
            for key, value in StoryResponse():
                setattr(self, key, getattr(self._db_obj, key))

        await session.refresh(self._db_obj, ['starting_location'])

    async def update(self, session: Any):
        for key, value in StoryData():
            setattr(self._db_obj, key, getattr(self, key))
        await session.commit()

    async def delete(self, session: Any):
        await session.refresh(self._db_obj, ['locations', 'characters'])
        await session.delete(self._db_obj)
        await session.commit()

    async def add_location(self, session: Any, location: Any):
        await session.refresh(self._db_obj, ['locations'])
        for db_location in self._db_obj.locations:
            if db_location.id == location.id:
                return
        self._db_obj.locations.append(location._db_obj)
        await session.commit()

    async def remove_location(self, session: Any, location: Any):
        await location.delete(session)
        await session.refresh(self._db_obj, ['locations'])

    async def locations(self, session: Any) -> List[LocationDb]:
        await session.refresh(self._db_obj, ['locations'])
        return self._db_obj.locations

    async def add_character(self, session: Any, character: Any):
        await session.refresh(self._db_obj, ['characters'])
        for db_character in self._db_obj.characters:
            if db_character.id == character.id:
                return
        self._db_obj.characters.append(character._db_obj)
        await session.commit()

    async def remove_character(self, session: Any, character: Any):
        await character.delete(session)
        await session.refresh(self._db_obj, ['characters'])

    async def characters(self, session: Any) -> List[CharacterDb]:
        await session.refresh(self._db_obj, ['characters'])
        return self._db_obj.characters


async def all_stories(session: Any, is_published: bool):
    if is_published is None:
        stmt = select(StoryDb)
    else:
        stmt = select(StoryDb).where(StoryDb.is_published == is_published)
    result = await session.execute(stmt)
    stories = []
    for db_story in result.scalars():
        story = Story(db_obj=db_story)
        await story.create(session)
        stories.append(story.model_dump(include=StoryResponse().model_dump()))
    return stories
