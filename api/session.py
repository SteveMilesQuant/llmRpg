import os
import asyncio
import aiohttp
from pydantic import PrivateAttr
from typing import Optional, Any, Dict, List
from sqlalchemy import select
from datamodels import SAMPLE_CHARACTERS, Object, SessionData, SessionResponse, SAMPLE_STORY, SAMPLE_LOCATIONS
from db import CharacterSessionDb, ChoiceDb, LocationsVisitedDb, SessionDb
from narrator import Narrator
from story import Story
from location import Location
from character import Character
from quest import QuestTracker, Quest


class Session(SessionResponse):
    _db_obj: Optional[SessionDb] = PrivateAttr()
    story: Optional[Story] = None
    locations_visited: Dict[int, bool] = {}
    current_character: Optional[Character] = None
    current_choices: List[str] = []

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
            data = self.model_dump(include=SessionData().model_dump())
            self._db_obj = SessionDb(**data)
            db_session.add(self._db_obj)
            await db_session.commit()
            self.id = self._db_obj.id
        else:
            # Otherwise, update attributes from fetched object
            for key, _ in SessionResponse():
                if key not in ['current_choices', 'locations_visited', 'quests', 'current_character', 'story']:
                    setattr(self, key, getattr(self._db_obj, key))

        await db_session.refresh(self._db_obj, ['current_choices', 'locations_visited', 'quests', 'current_character', 'story'])
        self.current_choices = [
            choice.choice for choice in self._db_obj.current_choices or []]
        self.locations_visited = {
            l.location_id: True for l in self._db_obj.locations_visited}
        if self._db_obj.current_character:
            self.current_character = Character(
                db_obj=self._db_obj.current_character)
            await self.current_character.create(db_session)
        self.quests = [Quest(db_obj=q) for q in self._db_obj.quests or []]
        for quest in self.quests:
            await quest.create(db_session)
        self.story = Story(db_obj=self._db_obj.story)
        await self.story.create(db_session)

    async def update_basic(self, db_session: Any):
        await db_session.refresh(self._db_obj, ['current_choices'])
        for choice_db in self._db_obj.current_choices:
            await db_session.delete(choice_db)
        for choice in self.current_choices:
            choice_db = ChoiceDb(session_id=self.id, choice=choice)
            db_session.add(choice_db)
            self._db_obj.current_choices.append(choice_db)
        for key, _ in SessionResponse():
            if key not in ['current_choices', 'locations_visited', 'quests', 'current_character', 'story']:
                setattr(self._db_obj, key, getattr(self, key))
        self._db_obj.current_character_id = self.current_character_id
        await db_session.commit()

        await db_session.refresh(self._db_obj, ['current_character', 'story'])
        self.current_character = Character(
            db_obj=self._db_obj.current_character)
        self.story = Story(db_obj=self._db_obj.story)
        await self.story.create(db_session)

    async def delete(self, db_session: Any):
        stmt = select(CharacterSessionDb).where(
            CharacterSessionDb.session_id == self.id)
        results = await db_session.execute(stmt)
        for result in results:
            await db_session.refresh(result[0], ['recent_history'])
            await db_session.delete(result[0])
        await db_session.refresh(self._db_obj, ['current_choices', 'locations_visited', 'quests'])
        await db_session.delete(self._db_obj)
        await db_session.commit()

    async def add_location(self, db_session: Optional[Any] = None, location_id: Optional[int] = None):
        if location_id is None or self.locations_visited.get(location_id):
            return
        if db_session:
            await db_session.refresh(self._db_obj, ['locations_visited'])
        loc_visited_db = LocationsVisitedDb(
            session_id=self.id,
            location_id=location_id
        )
        self.locations_visited[location_id] = True
        if db_session:
            db_session.add(loc_visited_db)
            self._db_obj.locations_visited.append(loc_visited_db)
            await db_session.commit()

    async def travel(
        self,
        openai_http_session: aiohttp.ClientSession,
        narrator: Narrator,
        tracker: QuestTracker,
        location: Optional[Location] = None,
        character: Optional[Character] = None,
        db_session: Optional[Any] = None
    ):
        narrator_expo = ""

        # Travel to a new location
        if self.current_character_id is None:
            # Entirely new adventure
            expo = await narrator.embark(openai_http_session)
            narrator_expo = narrator_expo + expo + '\n\n'
        else:
            # Just a new location
            expo = await narrator.travel(openai_http_session, self.current_character._db_obj.location, location)
            narrator_expo = narrator_expo + expo + '\n\n'

        # Describe that location and character, if it is our first time here
        if db_session:
            await character.prepare_session(db_session, self.id)
        if not self.locations_visited.get(location.id):
            expo = await narrator.arrive(openai_http_session, location)
            narrator_expo = narrator_expo + expo + '\n\n'

            expo = await narrator.meet(openai_http_session, character)
            narrator_expo = narrator_expo + expo + '\n\n'

            await self.add_location(db_session, location.id)
        else:
            expo = await narrator.remeet(openai_http_session, character)
            narrator_expo = narrator_expo + expo + '\n\n'

        # Update narrator memory
        narrator_expo = narrator_expo.strip()
        await narrator.update_memory(openai_http_session, f'Narrator: {narrator_expo}')

        # Generate choices
        self.current_choices = await character.offer_response_choices(openai_http_session, self.player_name, f'{filter(lambda q: q.issuer == character.name, tracker.quests)}')

        # Commit to database
        self.current_character_id = character.id
        self.narrator_memory = narrator.memory
        self.current_narration = narrator_expo
        if db_session:
            await self.update_basic(db_session)
        else:
            self.current_character = character

    async def interact(self,
                       openai_http_session: aiohttp.ClientSession,
                       narrator: Narrator,
                       tracker: QuestTracker,
                       user_input: str,
                       db_session: Optional[Any] = None):
        character = self.current_character
        if db_session:
            await character.prepare_session(db_session, self.id)
        character_response = await character.interact(openai_http_session, f'{filter(lambda q: q.watcher == character.name, tracker.quests)}', user_input, db_session)
        new_interaction = f'From {self.player_name} to {character.name}: """{user_input}"""\n\nFrom {character.name} to {self.player_name}: """{character_response}"""'
        await narrator.update_memory(openai_http_session, new_interaction)

        # Update quests
        await tracker.update_quests(
            openai_http_session,
            player_name=self.player_name,
            character_name=character.name,
            interactions=character._db_obj_session.recent_history,
            db_session=db_session
        )
        self.quests = tracker.quests

        # Generate choices
        self.current_choices = await character.offer_response_choices(openai_http_session, self.player_name, f'{filter(lambda q: q.issuer == character.name, tracker.quests)}')

        # Commit to database
        self.narrator_memory = narrator.memory
        self.current_narration = character_response
        if db_session:
            await self.update_basic(db_session)
            await db_session.commit()


async def main():
    # Options for this run
    verbose = True

    # HTTP configuration
    chat_url = "https://api.openai.com/v1/chat/completions"
    chat_model = "gpt-3.5-turbo"
    headers = {
        'content-type': 'application/json',
        'authorization': f'Bearer {os.environ.get("OPENAI_API_KEY")}'
    }

    # Initialize sample story
    player_name = 'Steve'
    session = Session(id=1, player_name=player_name)
    story = Story(**SAMPLE_STORY.model_dump())
    travel_to_location_id: Optional[int] = story.starting_location_id
    narrator = Narrator(
        chat_url=chat_url,
        chat_model=chat_model,
        player_name=player_name,
        story=story,
        memory="",
        verbose=verbose
    )
    tracker = QuestTracker(
        chat_url=chat_url,
        chat_model=chat_model,
        session_id=session.id,
        verbose=verbose
    )
    locations = [Location(**l.model_dump()) for l in SAMPLE_LOCATIONS]
    characters = [Character(**c.model_dump()) for c in SAMPLE_CHARACTERS]

    # Fake out database object information
    session.story = story
    story._db_obj = Object()
    for location in locations:
        if location.id == story.starting_location_id:
            story._db_obj.starting_location = location
            break
    for character in characters:
        character.green_room(
            chat_url=chat_url,
            chat_model=chat_model,
            verbose=verbose
        )
        character._db_obj = Object()
        character._db_obj.story = story
        for location in locations:
            if location.id == character.location_id:
                character._db_obj.location = location
                location._db_obj = Object()
                location._db_obj.starting_character = character
                break
        character._db_obj_session = Object()
        character._db_obj_session.id = 1
        character._db_obj_session.summarized_memory = ""
        character._db_obj_session.recent_history = []

    # Run the story simulation
    continueStory = True
    async with aiohttp.ClientSession(headers=headers) as openai_http_session:
        while (continueStory):
            if travel_to_location_id is not None:
                # Update local tracking for character and location
                for location in locations:
                    if location.id == travel_to_location_id:
                        break

                await session.travel(openai_http_session, narrator, location)

                travel_to_location_id = None
            else:
                await session.interact(openai_http_session, narrator, tracker, user_input)

            print('')
            user_input = input('Your choice: ')
            if user_input == "Q":
                continueStory = False
            if user_input == "T":
                user_prompt = 'Travel to location: '
                while travel_to_location_id is None:
                    location_name = input(user_prompt)
                    for location in locations:
                        if location.name.upper() == location_name.upper():
                            travel_to_location_id = location.id
                            break
                    user_prompt = f'Location not found ({location_name}). Try again: '

if __name__ == "__main__":
    asyncio.run(main())
