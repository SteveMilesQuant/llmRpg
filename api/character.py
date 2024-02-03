from pydantic import PrivateAttr
from typing import Optional, Any, List
from langchain.chains import ConversationChain
from langchain.prompts.prompt import PromptTemplate
from langchain.memory import ConversationSummaryMemory
from langchain_openai import OpenAI
from datamodels import CharacterResponse, LocationData
from db import CharacterDb

COMMMON_SUFFIX = '''

Previous conversation history:
{history}

New input: {input}

Response:
'''


class Character(CharacterResponse):
    _memory: Optional[ConversationSummaryMemory] = PrivateAttr()
    _conversation: Optional[ConversationChain] = PrivateAttr()
    _db_obj: Optional[CharacterDb] = PrivateAttr()

    def __init__(self, llm: Optional[OpenAI] = None, db_obj: Optional[CharacterDb] = None, story_setting: Optional[str] = None, locations: Optional[List[LocationData]] = None, **data):
        super().__init__(**data)
        self._db_obj = db_obj
        if llm:
            self._memory = ConversationSummaryMemory(llm=llm)

            setting_desc = 'SETTING:\n----------\n' + story_setting + '\n----------\n\n'
            locations_desc = 'LOCATIONS:\n----------\n'
            for location in locations:
                locations_desc = locations_desc + location.name + \
                    ': ' + location.description + '\n\n'
            locations_desc = locations_desc + '\n----------\n\n'

            character_template = self.description + '\n\n' + setting_desc + \
                locations_desc + COMMMON_SUFFIX
            character_prompt = PromptTemplate(
                input_variables=['history', 'input'],
                template=character_template
            )
            self._conversation = ConversationChain(
                llm=llm,
                prompt=character_prompt,
                memory=self._memory
            )

    async def create(self, session: Optional[Any]):
        if self._db_obj is None and self.id is not None:
            # Get by ID
            self._db_obj = await session.get(CharacterDb, [self.id])
            if self._db_obj is None:
                self.id = None
                return

        if self._db_obj is None:
            # If none found, create new
            character_data = self.dict(include=CharacterResponse().dict())
            self._db_obj = CharacterDb(**character_data)
            session.add(self._db_obj)
            await session.commit()
            self.id = self._db_obj.id
        else:
            # Otherwise, update attributes from fetched object
            for key, value in CharacterResponse():
                setattr(self, key, getattr(self._db_obj, key))

    async def update(self, session: Any):
        for key, value in CharacterResponse():
            setattr(self._db_obj, key, getattr(self, key))
        await session.commit()

    async def delete(self, session: Any):
        await session.delete(self._db_obj)
        await session.commit()

    def interact(self, interaction_desc: str) -> str:
        response = self._conversation.predict(input=interaction_desc)
        return response
