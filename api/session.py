from pydantic import PrivateAttr
from typing import Optional, Any, List
from datamodels import SessionData, SessionResponse
from db import SessionDb, ChoiceDb


class Session(SessionResponse):
    _db_obj: Optional[SessionDb] = PrivateAttr()

    def __init__(self, db_obj: Optional[SessionDb] = None, **data):
        super().__init__(**data)
        self._db_obj = db_obj

    async def create(self, db_session: Optional[Any]):
        if self._db_obj is None and self.id is not None:
            # Get by ID
            self._db_obj = await db_session.get(SessionDb, [self.id])
            if self._db_obj is None:
                self.id = None
                return

        if self._db_obj is None:
            # If none found, create new Session
            data = self.dict(include=SessionData().dict())
            self._db_obj = SessionDb(**data)
            db_session.add(self._db_obj)
            await db_session.commit()
            self.id = self._db_obj.id
        else:
            # Otherwise, update attributes from fetched object
            for key, value in SessionResponse():
                if key != 'current_choices':
                    setattr(self, key, getattr(self._db_obj, key))

        await db_session.refresh(self._db_obj, ['current_choices'])
        self.current_choices = [
            choice.choice for choice in self._db_obj.current_choices or []]

    async def update(self, db_session: Any):
        for key, value in SessionData():
            setattr(self._db_obj, key, getattr(self, key))
        await db_session.commit()

    async def delete(self, db_session: Any):
        await db_session.refresh(self._db_obj, ['current_choices'])
        await db_session.delete(self._db_obj)
        await db_session.commit()

    async def update_current_status(self, db_session: Any,
                                    current_character_id: Optional[int] = None,
                                    current_narration: Optional[str] = None,
                                    current_choices: Optional[List[str]] = None):
        if current_choices is not None:
            await db_session.refresh(self._db_obj, ['current_choices'])
            for db_choice in self._db_obj.current_choices or []:
                await db_session.delete(db_choice)
            await db_session.commit()
            for choice in current_choices:
                db_choice = ChoiceDb(session_id=self.id, choice=choice)
                db_session.add(db_choice)
        if current_character_id is not None:
            self._db_obj.currenct_character_id = current_character_id
        if current_narration is not None:
            self._db_obj.current_narration = current_narration
        await db_session.commit()
