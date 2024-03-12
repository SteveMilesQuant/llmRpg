import os
import asyncio
import aiohttp
from pydantic import PrivateAttr
from typing import Optional, Any, List, Dict
from datamodels import SAMPLE_CHARACTERS, CharacterBaseImage, Object, SessionData, SessionResponse, SAMPLE_STORY, SAMPLE_LOCATIONS
from db import CharacterBaseImagesDb, CharacterMemoryDb, CharacterRecentHistoryDb, LocationsVisitedDb, SessionDb, ChoiceDb
from narrator import Narrator
from story import Story
from location import Location
from character import Character
from quest import QuestTracker

CHARACTER_RECENT_HISTORY_LIMIT = 3


class Session(SessionResponse):
    _db_obj: Optional[SessionDb] = PrivateAttr()
    player_name: Optional[str] = None
    narrator_memory: Optional[str] = None
    character_memories: Dict[int, str] = {}
    character_recent_histories: Dict[int, List[str]] = {}
    character_base_images: Dict[int, CharacterBaseImage] = {}
    locations_visited: Dict[int, bool] = {}

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
                if key not in ['current_choices', 'character_memories', 'locations_visited', 'character_base_images']:
                    setattr(self, key, getattr(self._db_obj, key))

        await db_session.refresh(self._db_obj, ['current_choices', 'character_memories', 'locations_visited', 'character_recent_histories', 'character_base_images'])
        self.current_choices = [
            choice.choice for choice in self._db_obj.current_choices or []]
        self.character_memories = {
            m.character_id: m.memory_buffer for m in self._db_obj.character_memories}
        self.locations_visited = {
            location_id: True for location_id in self._db_obj.locations_visited}
        self.character_base_images = {
            i.character_id: CharacterBaseImage(id=i.character_id, url=i.base_image_url) for i in self._db_obj.character_base_images}
        self.character_recent_histories = {}
        for db_history in self._db_obj.character_recent_histories:
            hist_list = self.character_recent_histories.get(
                db_history.character_id)
            if hist_list is None:
                hist_list = []
                self.character_recent_histories[db_history.character_id] = hist_list
            hist_list.append(db_history.record)

    async def update_basic(self, db_session: Any):
        for key, value in SessionData():
            setattr(self._db_obj, key, getattr(self, key))
        await db_session.commit()

    async def delete(self, db_session: Any):
        await db_session.refresh(self._db_obj, ['current_choices', 'character_memories', 'locations_visited'])
        await db_session.delete(self._db_obj)
        await db_session.commit()

    async def add_location(self, db_session: Any, location_id: Optional[int] = None):
        if location_id is None or self.locations_visited.get(location_id):
            return
        await db_session.refresh(self._db_obj, ['locations_visited'])
        loc_visited_db = LocationsVisitedDb(
            session_id=self.id,
            location_id=location_id
        )
        db_session.add(loc_visited_db)
        self._db_obj.locations_visited.append(location_id)
        self.locations_visited[location_id] = True
        await db_session.commit()

    async def update_character_memory(self, db_session: Any, character_id: Optional[int] = None, character_memory: str = ""):
        if character_id is None:
            return
        await db_session.refresh(self._db_obj, ['character_memories'])
        if self.character_memories.get(character_id) is None:
            char_memory_db = CharacterMemoryDb(
                session_id=self.id,
                character_id=character_id,
                memory_buffer=character_memory
            )
            db_session.add(char_memory_db)
            self._db_obj.character_memories.append(char_memory_db)
        else:
            for char_memory_db in self._db_obj.character_memories:
                if char_memory_db.character_id == character_id:
                    char_memory_db.memory_buffer = character_memory
                    break
        self.character_memories[character_id] = character_memory
        await db_session.commit()

    async def add_character_recent_history(self, db_session: Any, character_id: Optional[int] = None, history_record: str = ""):
        if character_id is None:
            return
        await db_session.refresh(self._db_obj, ['character_recent_histories'])
        hist_list = self.character_recent_histories.get(character_id)
        if hist_list is None:
            hist_list = []
            self.character_recent_histories[character_id] = hist_list
        next_index = len(hist_list)
        if next_index < CHARACTER_RECENT_HISTORY_LIMIT:
            hist_list.append(history_record)
            hist_record_db = CharacterRecentHistoryDb(
                session_id=self.id,
                character_id=character_id,
                index=next_index,
                record=history_record
            )
            db_session.add(hist_record_db)
            self._db_obj.character_recent_histories.append(hist_record_db)
        else:
            hist_list.pop(0)
            hist_list.append(history_record)
            for hist_record_db in self._db_obj.character_recent_histories:
                if hist_record_db.session_id == self.id and hist_record_db.character_id == character_id:
                    hist_record_db.record = hist_list[hist_record_db.index]
        await db_session.commit()

    async def update_character_base_image(self, db_session: Any, character_id: Optional[int] = None, base_image: str = ""):
        if character_id is None:
            return
        await db_session.refresh(self._db_obj, ['character_base_images'])
        if self.character_base_images.get(character_id) is None:
            char_base_img_db = CharacterBaseImagesDb(
                session_id=self.id,
                character_id=character_id,
                base_image_url=base_image
            )
            db_session.add(char_base_img_db)
            self._db_obj.character_base_images.append(char_base_img_db)
        else:
            for char_base_img_db in self._db_obj.character_memories:
                if char_base_img_db.character_id == character_id:
                    char_base_img_db.base_image_url = base_image
                    break
        self.character_base_images[character_id] = CharacterBaseImage(
            id=character_id, url=base_image)
        await db_session.commit()
        return self.character_base_images[character_id]

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
            self.current_choices = current_choices
        if current_character_id is not None:
            self.current_character_id = current_character_id
            self._db_obj.current_character_id = current_character_id
        if current_narration is not None:
            self.current_narration = current_narration
            self._db_obj.current_narration = current_narration
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
    session = Session(player_name=player_name)
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
        chat_url=chat_url, chat_model=chat_model, verbose=verbose)
    locations = [Location(**l.model_dump()) for l in SAMPLE_LOCATIONS]
    characters = [Character(**c.model_dump()) for c in SAMPLE_CHARACTERS]
    current_location = None

    # Fake out database object information
    for character in characters:
        character.green_room(
            chat_url=chat_url,
            chat_model=chat_model,
            verbose=verbose,
            interactions_limit=2
        )
        character._db_obj = Object()
        character._db_obj.story = story
        for location in locations:
            if location.id == character.location_id:
                character._db_obj.location = location
                break

    # Run the story simulation
    continueStory = True
    async with aiohttp.ClientSession(headers=headers) as openai_http_session:
        while (continueStory):
            if travel_to_location_id is not None:
                narrator_expo = ""

                # Update local tracking for character and location
                last_location = current_location
                for character in characters:
                    if character.location_id == travel_to_location_id:
                        current_character = character
                        break
                current_location = current_character._db_obj.location

                # Travel to a new location
                if session.current_character_id is None:
                    # Entirely new adventure
                    expo = await narrator.embark(openai_http_session)
                    narrator_expo = narrator_expo + expo + '\n\n'

                else:
                    # Just a new location
                    expo = await narrator.travel(openai_http_session, last_location, current_location)
                    narrator_expo = narrator_expo + expo + '\n\n'
                session.current_character_id = current_character.id

                # Describe that location and character, if it is our first time here
                if not session.locations_visited.get(current_location.id):
                    expo = await narrator.arrive(openai_http_session, current_location)
                    narrator_expo = narrator_expo + expo + '\n\n'

                    expo = await narrator.meet(openai_http_session, current_character)
                    narrator_expo = narrator_expo + expo + '\n\n'

                    session.locations_visited[current_location.id] = True
                else:
                    expo = await narrator.remeet(openai_http_session, current_character)
                    narrator_expo = narrator_expo + expo + '\n\n'

                # Finally, update narrator memory and print result
                narrator_expo = narrator_expo.strip()
                await narrator.update_memory(openai_http_session, f'Narrator: {narrator_expo}')

                travel_to_location_id = None
            else:
                character_response = await current_character.interact(openai_http_session, filter(lambda q: q.watcher == current_character.name, tracker.quests), user_input)
                new_interaction = f'From {player_name} to {current_character.name}: """{user_input}"""\n\nFrom {current_character.name} to {player_name}: """{character_response}"""'
                await narrator.update_memory(openai_http_session, new_interaction)

                # Update quests
                await tracker.update_quests(
                    openai_http_session,
                    player_name=player_name,
                    character_name=current_character.name,
                    interactions=current_character._interactions
                )

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
