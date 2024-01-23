import os
import aiohttp
import json
from typing import Optional
from datetime import timedelta
from fastapi import FastAPI, APIRouter, Request, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from oauthlib.oauth2 import WebApplicationClient
from authentication import user_id_to_auth_token, auth_token_to_user_id
from db import init_db, close_db
from user import User
from session import Session


class Object(object):
    pass


description = """
API for managing the Level Up Learning business for scheduling summer and year-round
 educational track out camps. Guardians can define their students and enroll those
 students in camps. Instructors can design "programs" (i.e. curriculum) and "levels"
 (i.e. lessons) and see the camps they're currently teaching. Administrators can
 schedule camps, adjust enrollments, and assign instructors to camps.
"""
root_path = os.environ.get("API_ROOT_PATH") or ""
app = FastAPI(
    title="Level Up Learning",
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

    app.google_client = WebApplicationClient(app.config.GOOGLE_CLIENT_ID)

    app.db_engine, app.db_sessionmaker = await init_db(
        user=os.environ.get('DB_USER'),
        password=os.environ.get('DB_PASSWORD'),
        url=os.environ.get('DB_HOST'),
        port=os.environ.get('DB_PORT'),
        schema_name=os.environ.get('DB_SCHEMA_NAME'),
        for_pytest=(os.environ.get('PYTEST_RUN') == '1')
    )


@app.on_event('shutdown')
async def shutdown():
    await close_db(app.db_engine)


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
    if (user_info_json["sub"] != os.environ.get('ADMIN_USER_GOOGLE_ID')):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="User not authorized for admin privileges.")
    async with app.db_sessionmaker() as db_session:
        user = User(
            google_id=user_info_json["sub"]
        )
        await user.create(db_session)

        user_token, token_expiration = user_id_to_auth_token(app, user.id)
        return user_token


@api_router.post("/start")
async def session_start_post(request: Request):
    async with app.db_sessionmaker() as db_session:
        session = Session()
        await session.create(db_session)

        session_token, token_expiration = user_id_to_auth_token(
            app, session.id)
        return session_token


###############################################################################
# INCLUDE ROUTER (must go last)
###############################################################################


app.include_router(api_router)
