from pydantic import PrivateAttr
from typing import Optional, Any
from sqlalchemy import select
from datamodels import UserData, UserResponse
from db import UserDb


class User(UserResponse):
    google_id: Optional[str] = ''
    _db_obj: Optional[UserDb] = PrivateAttr()

    def __init__(self, db_obj: Optional[UserDb] = None, **data):
        super().__init__(**data)
        self._db_obj = db_obj

    async def create(self, session: Optional[Any]):
        if self._db_obj is None and self.id is not None:
            # Get by ID
            self._db_obj = await session.get(UserDb, [self.id])
            if self._db_obj is None:
                self.id = None
                return
        else:
            # Get by google id
            stmt = select(UserDb).where(UserDb.google_id == self.google_id)
            results = await session.execute(stmt)
            result = results.first()
            if result:
                self._db_obj = result[0]

        if self._db_obj is None:
            # If none found, create new user
            data = self.dict(include=UserData().dict())
            data['google_id'] = self.google_id
            self._db_obj = UserDb(**data)
            session.add(self._db_obj)
            await session.commit()
        else:
            # Otherwise, update attributes from fetched object
            for key, value in UserResponse():
                setattr(self, key, getattr(self._db_obj, key))
            self.google_id = self._db_obj.google_id

        # A couple cases require the id from the database (new or lookup by google_id)
        self.id = self._db_obj.id

    async def update(self, session: Any):
        for key, value in UserData():
            setattr(self._db_obj, key, getattr(self, key))
        await session.commit()

    async def delete(self, session: Any):
        await session.delete(self._db_obj)
        await session.commit()
