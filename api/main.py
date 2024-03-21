import os
import aiohttp
import json
from typing import Optional, List
from datetime import timedelta
from fastapi import FastAPI, APIRouter, Request, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from oauthlib.oauth2 import WebApplicationClient
from langchain_openai import OpenAI
from authentication import user_id_to_auth_token, auth_token_to_user_id
from db import init_db, close_db
from datamodels import Object, SessionResponse, ChoiceData
from datamodels import StoryData, StoryResponse, LocationData, LocationResponse
from datamodels import CharacterData, CharacterResponse, CharacterBaseImage
from user import User
from session import Session
from narrator import Narrator
from quest import QuestTracker
from story import Story, all_stories
from location import Location
from character import Character


description = """

"""
root_path = os.environ.get("API_ROOT_PATH") or ""
app = FastAPI(
    title="Location Up Learning",
    description=description,
    version="0.0.1",
    contact={
        "name": "Steve Miles",
        "url": "https://www.stevenmilesquant.com",
        "email": "steven.miles.quant@gmail.com",
    },
    docs_url=f'{root_path}/docs',
    openapi_url=f'{root_path}/openapi.json',
    redoc_url=None)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
api_router = APIRouter(prefix=root_path)


@app.on_event('startup')
async def startup():
    app.config = Object()
    app.config.secret_key = os.environ.get("SECRET_KEY") or os.urandom(24)
    app.config.GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", None)
    app.config.GOOGLE_CLIENT_SECRET = os.environ.get(
        "GOOGLE_CLIENT_SECRET", None)
    app.config.GOOGLE_DISCOVERY_URL = "https://accounts.google.com/.well-known/openid-configuration"
    app.config.jwt_lifetime = timedelta(days=1)
    app.config.jwt_algorithm = "HS256"
    app.config.jwt_subject = "access"
    app.config.chat_url = "https://api.openai.com/v1/chat/completions"
    app.config.chat_model = "gpt-3.5-turbo"

    app.google_client = WebApplicationClient(app.config.GOOGLE_CLIENT_ID)
    app.openai_headers = {
        'content-type': 'application/json',
        'authorization': f'Bearer {os.environ.get("OPENAI_API_KEY")}'
    }

    app.db_engine, app.db_sessionmaker = await init_db(
        user=os.environ.get('DB_USER'),
        password=os.environ.get('DB_PASSWORD'),
        url=os.environ.get('DB_HOST'),
        port=os.environ.get('DB_PORT'),
        schema_name=os.environ.get('DB_SCHEMA_NAME'),
        for_pytest=(os.environ.get('PYTEST_RUN') == '1')
    )

    app.llm = OpenAI(
        temperature=1, openai_api_key=os.environ.get('OPENAPI_API_KEY'), max_tokens=1024)


@app.on_event('shutdown')
async def shutdown():
    await close_db(app.db_engine)


###############################################################################
# USER MANAGEMENT (DESIGN ONLY)
###############################################################################


async def get_google_provider_cfg() -> dict:
    ret_json = {}
    async with aiohttp.ClientSession() as session:
        async with session.get(app.config.GOOGLE_DISCOVERY_URL) as response:
            ret_json = await response.json()
    return ret_json


async def get_authorized_user(request, session, required=True) -> Optional[User]:
    token = request.headers.get('Authorization')
    user_id = auth_token_to_user_id(app, token)
    if user_id:
        user = User(id=user_id)
        await user.create(session)
    else:
        user = None
    if required and (not user or user.id is None):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Auth: User not logged in.")
    return user


@api_router.post("/signin")
async def signin_post(request: Request, google_response_token: dict):
    '''Given the Google signin response token, returns this API's authentication token.'''
    google_provider_cfg = await get_google_provider_cfg()
    app.google_client.parse_request_body_response(
        json.dumps(google_response_token))
    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = app.google_client.add_token(userinfo_endpoint)
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(uri, data=body) as google_response:
            user_info_json = await google_response.json()
    if not user_info_json.get("email_verified"):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="User email not available or not verified by Google.")
    async with app.db_sessionmaker() as db_session:
        user = User(
            google_id=user_info_json["sub"]
        )
        await user.create(db_session)
        if user.id is None:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="User not authorized for admin privileges.")

        user_token, token_expiration = user_id_to_auth_token(app, user.id)
        return {"token": user_token, "expiration": token_expiration}


###############################################################################
# SESSION MANAGMENT
###############################################################################


async def get_session(request, db_session) -> Optional[Session]:
    token = request.headers.get('Session')
    if token is None:
        return None
    session_id = auth_token_to_user_id(app, token)
    if session_id:
        session = Session(id=session_id)
        await session.create(db_session)
        if session.id is None:
            session = None
    else:
        session = None
    return session


@api_router.post("/start/{story_id}")
async def session_start_post(request: Request, story_id: int):
    async with app.db_sessionmaker() as db_session:
        story = Story(id=story_id)
        await story.create(db_session)
        if story.id is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Story with id={story_id} not found.")

        session = await get_session(request, db_session)
        if session is None:
            session = Session(story_id=story.id)
            await session.create(db_session)
            if session.id is None:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                    detail=f"Session could not be created")

        session_token, token_expiration = user_id_to_auth_token(
            app, session.id)
        session.expiration = token_expiration
        await session.update_basic(db_session)
        return {"token": session_token, "expiration": token_expiration}


@api_router.put("/refresh")
async def session_refresh_put(request: Request):
    async with app.db_sessionmaker() as db_session:
        session = await get_session(request, db_session)
        if session is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Session not found. Start a new one.")

        session_token, token_expiration = user_id_to_auth_token(
            app, session.id)

        session.expiration = token_expiration
        await session.update_basic(db_session)

        return {"token": session_token, "expiration": token_expiration}


@api_router.delete("/stop")
async def session_stop_delete(request: Request):
    async with app.db_sessionmaker() as db_session:
        session = await get_session(request, db_session)
        if session is None:
            return
        await session.delete(db_session)


###############################################################################
# STORIES
###############################################################################


# Public route
@api_router.get("/stories", response_model=List[StoryResponse])
async def get_stories(request: Request, is_published: Optional[bool] = None):
    '''Get a list of stories. If the current user is an administrator, returns all stories.'''
    async with app.db_sessionmaker() as session:
        if not is_published:
            await get_authorized_user(request, session)
        return await all_stories(session, is_published)


# Public route
@api_router.get("/stories/{story_id}", response_model=StoryResponse)
async def get_story(request: Request, story_id: int):
    '''Get a single story.'''
    async with app.db_sessionmaker() as session:
        story = Story(id=story_id)
        await story.create(session)
        if story.id is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Story id={story_id} does not exist")
        return story


@api_router.put("/stories/{story_id}", response_model=StoryResponse)
async def put_update_story(request: Request, story_id: int, updated_story: StoryData):
    '''Update a story.'''
    async with app.db_sessionmaker() as session:
        await get_authorized_user(request, session)
        story = Story(id=story_id)
        await story.create(session)
        if story.id is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Story id={story_id} does not exist")
        story = story.copy(update=updated_story.dict(exclude_unset=True))
        await story.update(session)
        return story


@api_router.post("/stories", response_model=StoryResponse, status_code=status.HTTP_201_CREATED)
async def post_new_story(request: Request, new_story_data: StoryData):
    '''Create a new story.'''
    async with app.db_sessionmaker() as session:
        await get_authorized_user(request, session)
        new_story = Story(**new_story_data.dict())
        await new_story.create(session)
        if new_story.id is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Post new story failed")
        return new_story


@api_router.delete("/stories/{story_id}")
async def delete_story(request: Request, story_id: int):
    '''Delete a story.'''
    async with app.db_sessionmaker() as session:
        await get_authorized_user(request, session)
        story = Story(id=story_id)
        await story.create(session)
        if story.id is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Story id={story_id} does not exist")
        await story.delete(session)


###############################################################################
# STORIES -> LOCATIONS
###############################################################################


# Public route
@api_router.get("/stories/{story_id}/locations", response_model=List[LocationResponse])
async def get_locations(request: Request, story_id: int):
    '''Get all locations within a story.'''
    async with app.db_sessionmaker() as session:
        story = Story(id=story_id)
        await story.create(session)
        location_list = []
        for db_location in await story.locations(session):
            location = Location(db_obj=db_location)
            await location.create(session)
            location_list.append(location)
        return location_list


# Public route
@api_router.get("/stories/{story_id}/locations/{location_id}", response_model=LocationResponse)
async def get_location(request: Request, story_id: int, location_id: int):
    '''Get a single location within a story.'''
    async with app.db_sessionmaker() as session:
        story = Story(id=story_id)
        await story.create(session)
        if story.id is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Story id={story_id} does not exist")
        for db_location in await story.locations(session):
            if db_location.id == location_id:
                location = Location(db_obj=db_location)
                await location.create(session)
                return location
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Location id={location_id} does not exist for story id={story_id}")


@api_router.put("/stories/{story_id}/locations/{location_id}", response_model=LocationResponse)
async def put_update_location(request: Request, story_id: int, location_id: int, updated_location: LocationData):
    '''Update a location within a story.'''
    async with app.db_sessionmaker() as session:
        await get_authorized_user(request, session)
        story = Story(id=story_id)
        await story.create(session)
        if story.id is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Story id={story_id} does not exist")
        if story is None:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail=f"User does not have permission for story id={story_id}")
        for db_location in await story.locations(session):
            if db_location.id == location_id:
                location = Location(db_obj=db_location)
                await location.create(session)
                location = location.copy(
                    update=updated_location.dict(exclude_unset=True))
                await location.update(session)
                return location
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Location id={location_id} does not exist for story id={story_id}")


@api_router.post("/stories/{story_id}/locations", response_model=LocationResponse, status_code=status.HTTP_201_CREATED)
async def post_new_location(request: Request, story_id: int, new_location_data: LocationData):
    '''Create a new location within a story.'''
    async with app.db_sessionmaker() as session:
        await get_authorized_user(request, session)
        story = Story(id=story_id)
        await story.create(session)
        if story.id is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Story id={story_id} does not exist")
        if story is None:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail=f"User does not have permission for story id={story_id}")
        new_location = Location(**new_location_data.dict())
        await new_location.create(session)
        await story.add_location(session, new_location)
        return new_location


@api_router.delete("/stories/{story_id}/locations/{location_id}")
async def delete_location(request: Request, story_id: int, location_id: int):
    '''Remove a location from its story and delete it.'''
    async with app.db_sessionmaker() as session:
        await get_authorized_user(request, session)
        story = Story(id=story_id)
        await story.create(session)
        if story.id is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Story id={story_id} does not exist")
        if story is None:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail=f"User does not have permission for story id={story_id}")
        for db_location in await story.locations(session):
            if db_location.id == location_id:
                location = Location(db_obj=db_location)
                await location.create(session)
                await story.remove_location(session, location)
                return
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Location id={location_id} does not exist for story id={story_id}")


###############################################################################
# STORIES -> CHARACTERS
###############################################################################


# Public route
@api_router.get("/stories/{story_id}/characters", response_model=List[CharacterResponse])
async def get_characters(request: Request, story_id: int):
    '''Get all characters within a story.'''
    async with app.db_sessionmaker() as session:
        story = Story(id=story_id)
        await story.create(session)
        character_list = []
        for db_character in await story.characters(session):
            character = Character(db_obj=db_character)
            await character.create(session)
            character_list.append(character)
        return character_list


# Public route
@api_router.get("/stories/{story_id}/characters/{character_id}", response_model=CharacterResponse)
async def get_character(request: Request, story_id: int, character_id: int):
    '''Get a single character within a story.'''
    async with app.db_sessionmaker() as session:
        story = Story(id=story_id)
        await story.create(session)
        if story.id is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Story id={story_id} does not exist")
        for db_character in await story.characters(session):
            if db_character.id == character_id:
                character = Character(db_obj=db_character)
                await character.create(session)
                return character
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Character id={character_id} does not exist for story id={story_id}")


@api_router.put("/stories/{story_id}/characters/{character_id}", response_model=CharacterResponse)
async def put_update_character(request: Request, story_id: int, character_id: int, updated_character: CharacterData):
    '''Update a character within a story.'''
    async with app.db_sessionmaker() as session:
        await get_authorized_user(request, session)
        story = Story(id=story_id)
        await story.create(session)
        if story.id is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Story id={story_id} does not exist")
        if story is None:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail=f"User does not have permission for story id={story_id}")
        for db_character in await story.characters(session):
            if db_character.id == character_id:
                character = Character(db_obj=db_character)
                await character.create(session)
                character = character.copy(
                    update=updated_character.dict(exclude_unset=True))
                await character.update(session)
                return character
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Character id={character_id} does not exist for story id={story_id}")


@api_router.post("/stories/{story_id}/characters", response_model=CharacterResponse, status_code=status.HTTP_201_CREATED)
async def post_new_character(request: Request, story_id: int, new_character_data: CharacterData):
    '''Create a new character within a story.'''
    async with app.db_sessionmaker() as session:
        await get_authorized_user(request, session)
        story = Story(id=story_id)
        await story.create(session)
        if story.id is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Story id={story_id} does not exist")
        if story is None:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail=f"User does not have permission for story id={story_id}")
        new_character = Character(**new_character_data.dict())
        new_character.story_id = story_id
        await new_character.create(session)
        await story.add_character(session, new_character)
        return new_character


@api_router.delete("/stories/{story_id}/characters/{character_id}")
async def delete_character(request: Request, story_id: int, character_id: int):
    '''Remove a character from its story and delete it.'''
    async with app.db_sessionmaker() as session:
        await get_authorized_user(request, session)
        story = Story(id=story_id)
        await story.create(session)
        if story.id is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Story id={story_id} does not exist")
        if story is None:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail=f"User does not have permission for story id={story_id}")
        for db_character in await story.characters(session):
            if db_character.id == character_id:
                character = Character(db_obj=db_character)
                await character.create(session)
                await story.remove_character(session, character)
                return
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Character id={character_id} does not exist for story id={story_id}")


###############################################################################
# STORY SIMULATION
###############################################################################


# Public route, but session required
@api_router.get("/adventure", response_model=SessionResponse)
async def get_simulate(request: Request):
    '''Get the current status of the ongoing adventure.'''
    async with app.db_sessionmaker() as db_session:
        session = await get_session(request, db_session)
        if session is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Session not found. Start a new session.")
        return session


# Public route, but session required
@api_router.post("/interact", response_model=SessionResponse)
async def post_interact(request: Request, user_choice: ChoiceData):
    '''Make a single interaction in the adventure.'''
    async with aiohttp.ClientSession(headers=app.openai_headers) as openai_http_session:
        async with app.db_sessionmaker() as db_session:
            session = await get_session(request, db_session)
            if session is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                    detail=f"Session not found. Start a new session.")

            character = session.current_character
            character.green_room(
                chat_url=app.config.chat_url,
                chat_model=app.config.chat_model
            )

            narrator = Narrator(
                chat_url=app.config.chat_url,
                chat_model=app.config.chat_model,
                player_name=session.player_name,
                story=session.story,
                memory=session.narrator_memory
            )

            tracker = QuestTracker(
                chat_url=app.config.chat_url,
                chat_model=app.config.chat_model,
                session_id=session.id
            )
            await tracker.load_quests(db_session)

            await session.interact(openai_http_session, narrator, tracker, user_choice.choice, db_session)

            return session


# Public route, but session required
@api_router.post("/travel", response_model=SessionResponse)
async def post_travel(request: Request, user_choice: ChoiceData):
    '''Travel to a new location.'''
    async with aiohttp.ClientSession(headers=app.openai_headers) as openai_http_session:
        async with app.db_sessionmaker() as db_session:
            session = await get_session(request, db_session)
            if session is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                    detail=f"Session not found. Start a new session.")

            if session.current_character_id is None:
                # New adventure means
                if user_choice.choice is None:
                    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                        detail=f"When starting a new story, player name is required.")
                session.player_name = user_choice.choice
                new_location = Location(
                    db_obj=session.story._db_obj.starting_location)
                await new_location.create(db_session)
            else:
                if user_choice.location_id is None:
                    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                        detail=f"Location id={user_choice.location_id} does not exist")

                new_location = Location(id=user_choice.location_id)
                await new_location.create(db_session)
                if new_location.id is None:
                    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                        detail=f"Location id={user_choice.location_id} does not exist")

                await session.story.locations(db_session)
                if new_location._db_obj not in session.story._db_obj.locations:
                    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                        detail=f"Location id={new_location.id} is not within story with story id={session.story.id}")

            narrator = Narrator(
                chat_url=app.config.chat_url,
                chat_model=app.config.chat_model,
                player_name=session.player_name,
                story=session.story,
                memory=session.narrator_memory or ""
            )

            tracker = QuestTracker(
                chat_url=app.config.chat_url,
                chat_model=app.config.chat_model,
                session_id=session.id
            )
            await tracker.load_quests(db_session)

            new_character = Character(
                db_obj=new_location._db_obj.starting_character)
            await new_character.create(db_session)
            new_character.green_room(
                chat_url=app.config.chat_url,
                chat_model=app.config.chat_model,
            )

            await session.travel(openai_http_session, narrator, tracker, new_location, new_character, db_session)

            return session


# Public route, but session required
@api_router.get("/stories/{story_id}/characters/{character_id}/base_image", response_model=CharacterBaseImage)
async def get_character_base_image(request: Request, story_id: int, character_id: int):
    async with aiohttp.ClientSession(headers=app.openai_headers) as openai_http_session:
        async with app.db_sessionmaker() as db_session:
            session = await get_session(request, db_session)
            if session is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                    detail=f"Session not found. Start a new session.")

            character = Character(id=character_id)
            await character.create(db_session)
            if character.id is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                    detail=f"Character id={character_id} does not exist")
            if character._db_obj not in await session.story.characters(db_session):
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                    detail=f"Character id={character_id} does not exist for story id={story_id}")

            await character.prepare_session(db_session, session.id)
            image_url = await character.generate_base_image(openai_http_session, db_session)
            return CharacterBaseImage(id=character.id, url=image_url)


###############################################################################
# INCLUDE ROUTER (must go last)
###############################################################################


app.include_router(api_router)
