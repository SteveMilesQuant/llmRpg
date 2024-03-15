import aiohttp
import os
import asyncio
from pydantic import PrivateAttr
from sqlalchemy import delete, select
from typing import Optional, Any
from datamodels import SAMPLE_LOCATIONS, SAMPLE_STORY, CharacterData, CharacterResponse, SAMPLE_CHARACTERS, Object
from db import CharacterDb, CharacterRecentHistoryDb, CharacterSessionDb
from fastapi import HTTPException, status

CHARACTER_RECENT_HISTORY_LIMIT = 3

CHARACTER_TEMPLATE = '''You are a character in an interactive story. Your name is {character_name}. You live in {location_name} and are far too busy to leave there. The input you receive is from a human player. Your response should be the things you say and do in reply to the human player's input. Put the things you say in double quotes. If you have any open quests with the human, focus your responses on that.

{character_description}

Story setting:
---------------------------------
{story_setting}
---------------------------------

Description of the location {location_name} (where you live):
---------------------------------
{location_description}
---------------------------------

Previous conversation summary:
---------------------------------
{memory}
---------------------------------

Recent interactions:
---------------------------------
{recent_interactions}
---------------------------------

Ongoing quests you have requested:
---------------------------------
{quests}
---------------------------------
'''

CHARACTER_MEMORY_DESCRIPTION = '''You are someone the human is interacting with. You should summarize the interactions you have had with the human, merging new interactions in with old interactions. Try to be concise, but don't lose track of things the human has offered to do for you and whether they have done them. The input you receive is from the human.

Previous conversation summary: {interaction_summary}'''


IMAGE_GENERATOR_PROMPT_TEMPLATE = ''''Using a mythic fantasy art style, an image for the character described as follows. {image_desc}'''


def interaction_to_string(user_to_character: str, character_to_user: str):
    return f'''From me to you: {user_to_character}\nFrom you to me: {character_to_user}'''


class Character(CharacterResponse):
    _db_obj: Optional[CharacterDb] = PrivateAttr()
    _db_obj_session: Optional[CharacterSessionDb] = PrivateAttr()

    _verbose: Optional[bool] = PrivateAttr()
    _chat_url: Optional[str] = PrivateAttr()
    _chat_model: Optional[str] = PrivateAttr()
    _recent_history_limit: Optional[int] = PrivateAttr()

    def __init__(self, db_obj: Optional[CharacterDb] = None, **data):
        super().__init__(**data)
        self._db_obj = db_obj
        self._verbose = False
        self._chat_url = None
        self._chat_model = None
        self._recent_history_limit = CHARACTER_RECENT_HISTORY_LIMIT

    async def create(self, db_session: Optional[Any]):
        if self._db_obj is None and self.id is not None:
            # Get by ID
            self._db_obj = await db_session.get(CharacterDb, [self.id])
            if self._db_obj is None:
                self.id = None
                return

        if self._db_obj is None:
            # If none found, create new
            character_data = self.model_dump(
                include=CharacterResponse().model_dump())
            self._db_obj = CharacterDb(**character_data)
            db_session.add(self._db_obj)
            await db_session.commit()
            self.id = self._db_obj.id
        else:
            # Otherwise, update attributes from fetched object
            for key, _ in CharacterResponse():
                setattr(self, key, getattr(self._db_obj, key))

        await db_session.refresh(self._db_obj, ['location', 'story'])

    async def update(self, db_session: Any):
        for key, _ in CharacterData():
            setattr(self._db_obj, key, getattr(self, key))
        await db_session.commit()

    async def delete(self, db_session: Any):
        stmt = delete(CharacterSessionDb).where(
            CharacterSessionDb.character_id == self.id)
        await db_session.execute(stmt)
        await db_session.delete(self._db_obj)
        await db_session.commit()

    def green_room(self,
                   verbose: Optional[bool] = False,
                   chat_url: Optional[str] = None,
                   chat_model: Optional[str] = None) -> None:
        self._chat_url = chat_url
        self._chat_model = chat_model
        self._verbose = verbose

    async def prepare_session(self, db_session: Optional[Any], session_id: int):
        self._db_obj_session = None

        # Try to fetch it, if it exists
        stmt = select(CharacterSessionDb).where(
            CharacterSessionDb.session_id == session_id and CharacterSessionDb.character_id == self.id)
        results = await db_session.execute(stmt)
        result = results.first()
        if result:
            self._db_obj_session = result[0]

        # If not found, create new
        if self._db_obj_session is None:
            self._db_obj_session = CharacterSessionDb(
                session_id=session_id, character_id=self.id)
            db_session.add(self._db_obj_session)
            await db_session.commit()

        await db_session.refresh(self._db_obj_session, ['recent_history'])

    async def interact(self, openai_http_session: aiohttp.ClientSession, ongoing_quests: str, user_input: str, db_session: Optional[Any] = None) -> str:
        recent_interactions = '\n'.join(
            [interaction_to_string(i.user_input, i.character_response) for i in self._db_obj_session.recent_history])
        character_description = CHARACTER_TEMPLATE.format(
            character_name=self.name,
            character_description=self.private_description,
            story_setting=self._db_obj.story.setting,
            location_name=self._db_obj.location.name,
            location_description=self._db_obj.location.description,
            memory=self._db_obj_session.summarized_memory,
            recent_interactions=recent_interactions,
            quests=ongoing_quests
        )
        response = await openai_http_session.post(
            url=self._chat_url,
            json={
                "model": self._chat_model,
                "messages": [
                    {"role": "system", "content": character_description},
                    {"role": "user", "content": user_input}
                ],
                "temperature": 1
            })
        json = await response.json()
        character_response = json['choices'][0]['message']['content'].strip()
        if self._verbose:
            print(f'Player: {user_input}')
            print(f'{self.name}: {character_response}')
        await self.update_memory(openai_http_session, user_input, character_response, db_session)
        return character_response

    async def update_memory(self, openai_http_session: aiohttp.ClientSession, user_to_character: str, character_to_user: str, db_session: Optional[Any] = None) -> None:
        # Update the summarized memory, using
        memory_description = CHARACTER_MEMORY_DESCRIPTION.format(
            interaction_summary=self._db_obj_session.summarized_memory
        )
        interaction = interaction_to_string(
            user_to_character, character_to_user)
        response = await openai_http_session.post(
            url=self._chat_url,
            json={
                "model": self._chat_model,
                "messages": [
                    {"role": "system", "content": memory_description},
                    {"role": "user", "content": f'Merge this interaction into your previous conversation summary with me.\n\n{interaction}'}
                ],
                "temperature": 0
            })
        json = await response.json()
        json_msg = json['choices'][0]['message']
        self._db_obj_session.summarized_memory = json_msg['content'].strip()
        if db_session:
            await db_session.commit()

        # Add the new interaction
        new_index = max(
            [i.sort_index for i in self._db_obj_session.recent_history], default=0) + 1
        new_interaction = CharacterRecentHistoryDb(
            character_session_id=self._db_obj_session.id,
            sort_index=new_index,
            user_input=user_to_character,
            character_response=character_to_user
        )
        if db_session:
            await db_session.add(new_interaction)
            await db_session.commit()
            await db_session.refresh(self._db_obj_session, ['recent_history'])
        else:
            self._db_obj_session.recent_history.append(new_interaction)

        # Remove any old interactions that have gone past the limit
        while len(self._db_obj_session.recent_history) > self._recent_history_limit:
            remove_history = self._db_obj_session.recent_history.pop(0)
            if db_session:
                await db_session.delete(remove_history)

        # Print, if verbose
        if self._verbose:
            print(f'{self.name} memory: {self._db_obj_session.summarized_memory}')
            print(f'{self.name} recent history:')
            for interaction in self._db_obj_session.recent_history:
                print(
                    f'\t({interaction.user_input}, {interaction.character_response})')

    async def generate_base_image(self, openai_http_session: aiohttp.ClientSession, db_session: Optional[Any] = None) -> str:
        if self._db_obj_session.base_image_url is None:
            response = await openai_http_session.post(
                url="https://api.openai.com/v1/images/generations",
                json={
                    "model": "dall-e-3",
                    "prompt": IMAGE_GENERATOR_PROMPT_TEMPLATE.format(image_desc=self.public_description),
                    "n": 1,
                    "size": "1024x1024",
                    "quality": "hd"
                },
            )
            json = await response.json()
            error = json.get('error')
            if error:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                    detail=f"Error reported from open ai: {error['message']}")
            self._db_obj_session.base_image_url = json['data'][0]['url']
            if db_session:
                await db_session.commit()
        return self._db_obj_session.base_image_url


async def main():
    verbose = True

    # HTTP configuration
    chat_url = "https://api.openai.com/v1/chat/completions"
    chat_model = "gpt-3.5-turbo"
    headers = {
        'content-type': 'application/json',
        'authorization': f'Bearer {os.environ.get("OPENAI_API_KEY")}'
    }

    # Story elements
    story = SAMPLE_STORY
    locations = SAMPLE_LOCATIONS
    character = Character(**SAMPLE_CHARACTERS[0].model_dump())
    character._recent_history_limit = 2
    character.green_room(
        chat_url=chat_url,
        chat_model=chat_model,
        verbose=verbose
    )

    # Fake out database object information
    character._db_obj = Object()
    character._db_obj.story = story
    for location in locations:
        if location.id == character.location_id:
            character._db_obj.location = location
            break
    character._db_obj_session = Object()
    character._db_obj_session.id = 1
    character._db_obj_session.summarized_memory = ""
    character._db_obj_session.recent_history = []

    interactions = [
        '''"Hello!"''',
        '''"I'm just passing through. Is there anything I can help you with?"''',
        '''"Yes, of course."''',
        '''"I'll be on my way now. Goodbye."''',
    ]

    # Test interactions with this character
    async with aiohttp.ClientSession(headers=headers) as openai_http_session:
        for interaction in interactions:
            await character.interact(openai_http_session, "", interaction)
            print('')


if __name__ == "__main__":
    asyncio.run(main())
