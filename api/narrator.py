import os
import aiohttp
import asyncio
from pydantic import BaseModel
from story import Story
from location import Location
from character import Character
from datamodels import SAMPLE_CHARACTERS, SAMPLE_LOCATIONS, SAMPLE_STORY


NARRATOR_DESCRIPTION = '''You are the narrator of an interactive story. The input you receive is from a Player playing as the main character of this story. Your response should describe what the Player sees, hears, and perhaps says (if provided by the Player), and should use descriptive or creative language, but should generally be brief (2-5 sentences).'''

EMBARK_TEMPLATE = '''I am just starting this story as a traveler from outside the realm and I know nothing about this land. Summarize the following setting to me.

Story setting: {story_setting}'''

TRAVEL_TEMPLATE = '''I'm traveling from location {from_location_name} to location {to_location_name}. Summarize my travel between these locations.

{from_location_name} description: {from_location_desc}

{to_location_name} description: {to_location_desc}'''

ARRIVE_TEMPLATE = '''I arrive at {location_name}, which I have not been to before. Summarize that location to me according to the following description. Do not begin your response with "As".

{location_name}: {location_description}'''

MEET_TEMPLATE = '''I prepare to interact with {character_name}, whom I have not met. Summarize that person to me according to the following description. Do not begin your response with "As".

{character_name}: {character_description}'''

REMEET_TEMPLATE = '''I prepare to interact with {character_name}, whom I have already meet. Describe how they react as I approach. Do not begin your response with "As".

{character_name}'s description: {character_description}'''

NARRATOR_MEMORY_DESCRIPTION = '''You summarize events and descriptions given to you into a concise account of general events. You will receive new interactions between a Human named "{player_name}" and other characters. One such character is the Narrator, who is always speaking directly to {player_name} and will refer to {player_name} as "you". Your summary should use the past tense and third person describing what {player_name} as done, seen, and said. You should ignore descriptive details and summarize into a concise account of general events.

Past summary: {story_summary}'''


class Narrator(BaseModel):
    player_name: str = None
    story: Story = None
    memory: str = ""
    verbose: bool = False
    chat_url: str = "https://api.openai.com/v1/chat/completions"
    chat_model: str = "gpt-3.5-turbo"

    async def _post_query(self, openai_http_session: aiohttp.ClientSession, query: str) -> str:
        response = await openai_http_session.post(
            url=self.chat_url,
            json={
                "model": self.chat_model,
                "messages": [
                    {"role": "system", "content": NARRATOR_DESCRIPTION},
                    {"role": "user", "content": query}
                ],
                "temperature": 1
            })
        json = await response.json()
        expo = json['choices'][0]['message']['content'].strip()
        if self.verbose:
            print(f'Narrator: {expo}')
        return expo

    async def update_memory(self, openai_http_session: aiohttp.ClientSession, new_interaction: str) -> None:
        memory_query = NARRATOR_MEMORY_DESCRIPTION.format(
            player_name=self.player_name,
            story_summary=self.memory
        )
        response = await openai_http_session.post(
            url=self.chat_url,
            json={
                "model": self.chat_model,
                "messages": [
                    {"role": "system", "content": memory_query},
                    {"role": "user", "content": f'Merge this interaction into your past summary and give me a new summary. """{new_interaction}"""'}
                ],
                "temperature": 0
            })
        json = await response.json()
        self.memory = json['choices'][0]['message']['content'].strip()
        if self.verbose:
            print(f'Narrator memory: {self.memory}')

    async def embark(self, openai_http_session: aiohttp.ClientSession) -> str:
        new_query = EMBARK_TEMPLATE.format(
            story_summary=self.memory,
            story_setting=self.story.setting
        )
        return await self._post_query(openai_http_session, new_query)

    async def travel(self, openai_http_session: aiohttp.ClientSession, from_location: Location, to_location: Location) -> str:
        new_query = TRAVEL_TEMPLATE.format(
            from_location_name=from_location.name,
            from_location_desc=from_location.description,
            to_location_name=to_location.name,
            to_location_desc=to_location.description
        )
        return await self._post_query(openai_http_session, new_query)

    async def arrive(self, openai_http_session: aiohttp.ClientSession, location: Location) -> str:
        new_query = ARRIVE_TEMPLATE.format(
            location_name=location.name,
            location_description=location.description
        )
        return await self._post_query(openai_http_session, new_query)

    async def meet(self, openai_http_session: aiohttp.ClientSession, character: Character) -> str:
        new_query = MEET_TEMPLATE.format(
            character_name=character.name,
            character_description=character.public_description
        )
        return await self._post_query(openai_http_session, new_query)

    async def remeet(self, openai_http_session: aiohttp.ClientSession, character: Character) -> str:
        new_query = REMEET_TEMPLATE.format(
            character_name=character.name,
            character_description=character.public_description
        )
        return await self._post_query(openai_http_session, new_query)


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
    player_name = 'Steve'
    story = Story(**SAMPLE_STORY.model_dump())
    narrator = Narrator(
        chat_url=chat_url,
        chat_model=chat_model,
        player_name=player_name,
        story=story,
        memory="",
        verbose=verbose
    )
    locations = [Location(**l.model_dump()) for l in SAMPLE_LOCATIONS]
    characters = [Character(**c.model_dump()) for c in SAMPLE_CHARACTERS]

    # Test arrive
    async with aiohttp.ClientSession(headers=headers) as openai_http_session:
        embark_expo = await narrator.embark(openai_http_session)
        await narrator.update_memory(openai_http_session, f'Narrator: {embark_expo}')
        print('')

        arrival_expo = await narrator.arrive(openai_http_session, locations[0])
        await narrator.update_memory(openai_http_session, f'Narrator: {arrival_expo}')
        print('')

        travel_expo = await narrator.travel(openai_http_session, locations[0], locations[1])
        await narrator.update_memory(openai_http_session, f'Narrator: {travel_expo}')
        print('')

        meet_expo = await narrator.meet(openai_http_session, characters[0])
        await narrator.update_memory(openai_http_session, f'Narrator: {meet_expo}')
        print('')

        remeet_expo = await narrator.remeet(openai_http_session, characters[0])
        await narrator.update_memory(openai_http_session, f'Narrator: {remeet_expo}')
        print('')


if __name__ == "__main__":
    asyncio.run(main())
