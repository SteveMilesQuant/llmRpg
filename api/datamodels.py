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


class StoryData(BaseModel):
    '''Story data'''
    title: Optional[str] = ""
    setting: Optional[str] = ""
    is_published: Optional[bool] = False


class StoryResponse(StoryData):
    '''Story response'''
    id: Optional[int] = None


class LocationData(BaseModel):
    '''Location data'''
    name: Optional[str] = ""
    description: Optional[str] = ""


class LocationResponse(LocationData):
    '''Location response'''
    id: Optional[int] = None
    story_id: Optional[int] = None


class CharacterData(BaseModel):
    '''Character data'''
    name: Optional[str] = ""
    description: Optional[str] = ""


class CharacterResponse(CharacterData):
    '''Character response'''
    id: Optional[int] = None
    story_id: Optional[int] = None
