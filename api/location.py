from pydantic import PrivateAttr
from typing import Optional, Any
from datamodels import LocationResponse
from db import LocationDb


class Location(LocationResponse):
    _db_obj: Optional[LocationDb] = PrivateAttr()

    def __init__(self, db_obj: Optional[LocationDb] = None, **data):
        super().__init__(**data)
        self._db_obj = db_obj

    async def create(self, session: Optional[Any]):
        if self._db_obj is None and self.id is not None:
            # Get by ID
            self._db_obj = await session.get(LocationDb, [self.id])
            if self._db_obj is None:
                self.id = None
                return

        if self._db_obj is None:
            # If none found, create new
            location_data = self.dict(include=LocationResponse().dict())
            self._db_obj = LocationDb(**location_data)
            session.add(self._db_obj)
            await session.commit()
            self.id = self._db_obj.id
        else:
            # Otherwise, update attributes from fetched object
            for key, value in LocationResponse():
                setattr(self, key, getattr(self._db_obj, key))

        await session.refresh(self._db_obj, ['starting_character'])

    async def update(self, session: Any):
        for key, value in LocationResponse():
            setattr(self._db_obj, key, getattr(self, key))
        await session.commit()

    async def delete(self, session: Any):
        await session.delete(self._db_obj)
        await session.commit()
