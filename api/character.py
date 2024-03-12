import aiohttp
import os
import asyncio
from pydantic import PrivateAttr
from typing import Optional, Any, List
from datamodels import SAMPLE_LOCATIONS, SAMPLE_STORY, CharacterResponse, SAMPLE_CHARACTERS, Object
from db import CharacterDb
from fastapi import HTTPException, status


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
    _verbose: Optional[bool] = PrivateAttr()
    _chat_url: Optional[str] = PrivateAttr()
    _chat_model: Optional[str] = PrivateAttr()
    _memory: Optional[str] = PrivateAttr()
    _interactions: Optional[List[tuple[str, str]]] = PrivateAttr()
    _interactions_limit: Optional[int] = PrivateAttr()
    _base_image: Optional[str] = PrivateAttr()

    def __init__(self, db_obj: Optional[CharacterDb] = None, **data):
        super().__init__(**data)
        self._db_obj = db_obj
        self._verbose = False
        self._chat_url = None
        self._chat_model = None
        self._memory = ""
        self._interactions = []
        self._interactions_limit = 0
        self._base_image = None

    async def create(self, session: Optional[Any]):
        if self._db_obj is None and self.id is not None:
            # Get by ID
            self._db_obj = await session.get(CharacterDb, [self.id])
            if self._db_obj is None:
                self.id = None
                return

        if self._db_obj is None:
            # If none found, create new
            character_data = self.model_dump(
                include=CharacterResponse().model_dump())
            self._db_obj = CharacterDb(**character_data)
            session.add(self._db_obj)
            await session.commit()
            self.id = self._db_obj.id
        else:
            # Otherwise, update attributes from fetched object
            for key, _ in CharacterResponse():
                setattr(self, key, getattr(self._db_obj, key))

        await session.refresh(self._db_obj, ['location', 'story'])

    def green_room(self,
                   chat_url: Optional[str] = None,
                   chat_model: Optional[str] = None,
                   verbose: Optional[bool] = False,
                   memory: Optional[str] = "",
                   interactions: Optional[List[str]] = [],
                   interactions_limit: Optional[int] = 0
                   ) -> None:
        self._chat_url = chat_url
        self._chat_model = chat_model
        self._verbose = verbose
        self._memory = memory
        self._interactions = interactions or []
        self._interactions_limit = interactions_limit

    async def interact(self, openai_http_session: aiohttp.ClientSession, ongoing_quests: str, user_input: str) -> str:
        recent_interactions = '\n'.join(
            [interaction_to_string(i[0], i[1]) for i in self._interactions])
        character_description = CHARACTER_TEMPLATE.format(
            character_name=self.name,
            character_description=self.private_description,
            story_setting=self._db_obj.story.setting,
            location_name=self._db_obj.location.name,
            location_description=self._db_obj.location.description,
            memory=self._memory,
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
        await self.update_memory(openai_http_session, user_input, character_response)
        return character_response

    async def update_memory(self, openai_http_session: aiohttp.ClientSession, user_to_character: str, character_to_user: str) -> None:
        memory_description = CHARACTER_MEMORY_DESCRIPTION.format(
            interaction_summary=self._memory
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
        self._memory = json['choices'][0]['message']['content'].strip()
        self._interactions.append((user_to_character, character_to_user))
        while len(self._interactions) > self._interactions_limit:
            self._interactions.pop(0)
        if self._verbose:
            print(f'{self.name} memory: {self._memory}')
            print(f'{self.name} interactions: {self._interactions}')

    async def generate_base_image(self, openai_http_session: aiohttp.ClientSession) -> str:
        if self._base_image:
            # TODO: instead generate a new image based off of that one
            return self._base_image
        else:
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
            return json['data'][0]['url']


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
    character.green_room(
        chat_url=chat_url,
        chat_model=chat_model,
        verbose=verbose,
        interactions_limit=2
    )

    # Fake out database object information
    character._db_obj = Object()
    character._db_obj.story = story
    for location in locations:
        if location.id == character.location_id:
            character._db_obj.location = location
            break

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
