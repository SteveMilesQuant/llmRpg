from pydantic import PrivateAttr
from ast import literal_eval
from typing import Optional, Any, List
from langchain.chains import ConversationChain
from langchain.prompts.prompt import PromptTemplate
from langchain.memory import ConversationSummaryMemory, ConversationBufferWindowMemory
from langchain_openai import OpenAI
from datamodels import CharacterResponse, LocationData
from db import CharacterDb
from location import Location


CHARACTER_TEMPLATE = '''You are a character in an interactive story. Your name is {character_name}. You live in {location_name}. The input you receive is from a human Player. Your response should be the things you say and do in reply to the Players's input. Put the things you say in double quotes.

{character_description}

Story setting:
{story_setting}

Description of the location {location_name} (where you live):
{location_description}

Previous conversation history:
{history}

New input: {input}

Response:
'''

OFFERER_TEMPLATE = '''You generate interactive choices for the human Player, who is playing an interactive story. The input you receive is from this human Player, who will describe the most recent interaction they've had with the character {character_name}. Your response should be four choices that you offer the Player. The choices can be things the player can say to the character they're interacting with, which should be encapsulated in double quotes, and/or things the player can do in that moment, which would not be in double quotes. Offer the Player choices that are appropriate to the situation and character they are interacting with.

You MUST format your response as a Python array of strings. For example,
[
   \'\'\'First choice\'\'\',
   \'\'\'Second choice with "quoted dialog"\'\'\',
   etc.
]

{history}

New input:
------------------------------
{input}
------------------------------

Response:
'''

OFFER_HISTORY_TEMPLATE = '''Story summary:
------------------------------
{story_summary}
------------------------------

Previous conversation history:
------------------------------
{history}
------------------------------'''


class Character(CharacterResponse):
    _memory: Optional[ConversationSummaryMemory] = PrivateAttr()
    _conversation: Optional[ConversationChain] = PrivateAttr()
    _offerer: Optional[ConversationChain] = PrivateAttr()
    _db_obj: Optional[CharacterDb] = PrivateAttr()
    _interactions: Optional[List[str]] = PrivateAttr()
    _last_interaction: Optional[str] = PrivateAttr()

    def __init__(self, db_obj: Optional[CharacterDb] = None, **data):
        super().__init__(**data)
        self._db_obj = db_obj
        self._interactions = []

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

        await session.refresh(self._db_obj, ['location', 'story'])

    def green_room(self, llm: Optional[OpenAI] = None):
        self._memory = ConversationSummaryMemory(llm=llm)

        character_template = CHARACTER_TEMPLATE.format(
            input='{input}',
            history='{history}',
            character_name=self.name,
            character_description=self.private_description,
            location_name=self._db_obj.location.name,
            location_description=self._db_obj.location.description,
            story_setting=self._db_obj.story.setting
        )
        character_prompt = PromptTemplate(
            input_variables=['history', 'input'],
            template=character_template
        )
        self._conversation = ConversationChain(
            llm=llm,
            prompt=character_prompt,
            memory=self._memory
        )

        offer_template = OFFERER_TEMPLATE.format(
            input='{input}',
            history='{history}',
            character_name=self.name
        )
        offer_prompt = PromptTemplate(
            input_variables=['history', 'input'],
            template=offer_template
        )
        self._offerer = ConversationChain(
            llm=llm,
            prompt=offer_prompt
        )

    async def update(self, session: Any):
        for key, value in CharacterResponse():
            setattr(self._db_obj, key, getattr(self, key))
        await session.commit()

    async def delete(self, session: Any):
        await session.delete(self._db_obj)
        await session.commit()

    def interact(self, interaction_desc: str) -> str:
        response = self._conversation.invoke({'input': interaction_desc})
        character_response = response['response']
        self._last_interaction = f"\nFrom the Player to {self.name}: {interaction_desc}\n\n From {self.name} to the Player: {character_response}"
        return character_response

    def offer(self, story_summary: str) -> List[str]:
        if (self._last_interaction) is None:
            return []

        history = ''
        for interaction in self._interactions:
            history = history + interaction + '\n\n'

        history_formatted = OFFER_HISTORY_TEMPLATE.format(
            history=history,
            story_summary=story_summary
        )

        response = self._offerer.invoke({
            'input': f'Give me choices for replying to my last interaction with {self.name}, which is as follows:\n' + self._last_interaction,
            'history': history_formatted
        })
        offer_response = response['response']

        try:
            choices = literal_eval(offer_response)
        except:
            response = self._offerer.invoke({
                'input': f'Your last response was not formatted correctly. Please reformat. Your last response was:\n{offer_response}',
                'history': history_formatted
            })
            offer_response = response['response']
            choices = literal_eval(offer_response)

        self._interactions.append(self._last_interaction)
        self._last_interaction = None

        return choices
