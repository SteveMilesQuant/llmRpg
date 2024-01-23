from pydantic import BaseModel
from typing import Optional, Tuple, List
from datetime import date, datetime, time
from enum import Enum


class FastApiDate(date):
    def __str__(self) -> str:
        return self.strftime('%Y-%m-%d')


class FastApiDatetime(datetime):
    def __str__(self) -> str:
        return self.strftime('%Y-%m-%dT%H:%M:%S')


class FastApiTime(time):
    def __str__(self) -> str:
        return self.strftime('%H:%M:%S')


class UserData(BaseModel):
    '''User data'''


class UserResponse(UserData):
    '''User response'''
    id: Optional[int] = None


class SessionData(BaseModel):
    '''Session data'''
    expiration: Optional[datetime] = None


class SessionResponse(SessionData):
    '''Session response'''
    id: Optional[int] = None
