from pydantic import PrivateAttr
from typing import Optional, Any
from datamodels import SessionData, SessionResponse
from db import SessionDb


class Session(SessionResponse):
    _db_obj: Optional[SessionDb] = PrivateAttr()

    def __init__(self, db_obj: Optional[SessionDb] = None, **data):
        super().__init__(**data)
        self._db_obj = db_obj

    async def create(self, session: Optional[Any]):
        if self._db_obj is None and self.id is not None:
            # Get by ID
            self._db_obj = await session.get(SessionDb, [self.id])
            if self._db_obj is None:
                self.id = None
                return

        if self._db_obj is None:
            # If none found, create new Session
            data = self.dict(include=SessionData().dict())
            self._db_obj = SessionDb(**data)
            session.add(self._db_obj)
            await session.commit()
        else:
            # Otherwise, update attributes from fetched object
            for key, value in SessionResponse():
                setattr(self, key, getattr(self._db_obj, key))

        # A couple cases require the id from the database (new or lookup by google_id)
        self.id = self._db_obj.id

    async def update(self, session: Any):
        for key, value in SessionData():
            setattr(self._db_obj, key, getattr(self, key))
        await session.commit()

    async def delete(self, session: Any):
        await session.delete(self._db_obj)
        await session.commit()
