import os
import asyncio
from typing import Optional
from langchain.chains import ConversationChain
from langchain.prompts.prompt import PromptTemplate
from langchain.memory import ConversationSummaryMemory
from langchain_openai import OpenAI
from langchain.agents import AgentExecutor, create_react_agent, load_tools
from datamodels import Object, SAMPLE_CHARACTERS, SAMPLE_LOCATIONS, SAMPLE_STORY
from story import Story
from location import Location
from character import Character


NARRATOR_TEMPLATE = '''You are the narrator of an interactive story. The input you receive is from a Player playing as the main character of this story. Your response should describe what the Player sees, hears, and perhaps says (if provided by the Player), and should use descriptive or creative language, but should generally be brief (2-5 sentences).

Previous conversation history:
------------------------------
{history}
------------------------------

New input:
------------------------------
{input}
------------------------------

Response:
'''

IMAGE_GENERATOR_PROMPT_TEMPLATE = ''''Generate a 240px by 240px image based on the provided description. Use an animated art style, as would be fitting for a children's story. Ensure any character faces have detail and are not blurry and do not look like monsters. Ensure the image is 240px by 240px. You have access to the following tools:

{tools}

Use the following format:

Description: the input description of the image you must generate
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the url for the image you have generated

Begin!

Description: {input}
Thought:{agent_scratchpad}'''


class Narrator:
    def __init__(self, llm: Optional[OpenAI] = None, memory_buffer: Optional[ConversationSummaryMemory] = None):
        self.llm = llm
        if memory_buffer is not None:
            self.memory = ConversationSummaryMemory(
                llm=llm, buffer=memory_buffer)
        else:
            self.memory = ConversationSummaryMemory(llm=llm)

        prompt = PromptTemplate(
            input_variables=['history', 'input'],
            template=NARRATOR_TEMPLATE
        )
        self.expositioner = ConversationChain(
            llm=llm,
            prompt=prompt,
            memory=self.memory
        )

    async def embark(self, player_name: str, story: Story, location: Location, character: Character):
        response = await self.expositioner.ainvoke({
            "input": f'My name is {player_name}. I am just starting this story as a traveler from outside the realm and I know nothing about this land. Summarize the following setting to me.\n\nSETTING: {story.setting}'
        })
        land_expo = response['response']

        response = await self.expositioner.ainvoke({
            "input": f'I arrive at {location.name}. Summarize that location to me according to the following description.\n\n\{location.name}: {location.description}'
        })
        location_expo = response['response']

        response = await self.expositioner.ainvoke({
            "input": f'I prepare to interact with {character.name}, whom I have not met. Summarize that person to me according to the following description.\n\n\{character.name}: {character.public_description}'
        })
        character_expo = response['response']

        choices = [
            f'''"Hello, my name is {player_name}. I'm just passing through this area, but I'm looking for opportunities to help people."''',
            f'''"Hello, my name is {player_name}. I'm just passing through this area, but I'm looking for opportunities to make money."'''
        ]

        return {"exposition": land_expo + '\n\n' + location_expo + '\n\n' + character_expo, "choices": choices}

    async def interact(self, character: Character, interaction_desc: str):
        character_response = await character.interact(interaction_desc)
        response = await self.expositioner.ainvoke({
            "input": f'The following interaction just occurred. Please describe it to me. Quote {character.name}\'s response into your description. \n\nI said to {character.name}: {interaction_desc}\n\n{character.name}\'s response to me: {character_response}'
        })
        choices = await character.offer(self.memory.buffer)
        return {"exposition": response['response'], "choices": choices}

    async def travel(self, player_name: str, previous_character: Character, new_location: Location, first_time_visiting: bool = True):
        previous_location = previous_character._db_obj.location
        new_character = new_location._db_obj.starting_character

        goodbye = '''"Sorry, but I feel I must move on now. It will be quite a while before I return. Goodbye.'''
        goodbye_response = await previous_character.interact(goodbye)
        response = await self.expositioner.ainvoke({
            "input": f'The following interaction just occurred. Please describe it to me. Quote {previous_character.name}\'s response into your description. \n\nI say to {previous_character.name}: {goodbye}\n\n{previous_character.name}\'s response to me: {goodbye_response}'
        })
        goodbye_expo = response['response']

        response = await self.expositioner.ainvoke({
            "input": f'Summarize traveling along the road from {previous_location.name} to {new_location.name}. The new location is described below.\n\n{new_location.name}:{new_location.description}'
        })
        travel_expo = response['response']

        if first_time_visiting:
            response = await self.expositioner.ainvoke({
                "input": f'I prepare to interact with {new_character.name}, whom I have not met. Summarize that person to me according to the following description.\n\n\{new_character.name}: {new_character.public_description}'
            })
            character_expo = response['response']
        else:
            character_expo = ""

        if first_time_visiting:
            choices = [
                f'''"Hello, my name is {player_name}. I'm just passing through this area, but I'm looking for opportunities to help people."''',
                f'''"Hello, my name is {player_name}. I'm just passing through this area, but I'm looking for opportunities to make money."'''
            ]
        else:
            choices = await new_character.offer(self.memory.buffer)

        exposition = goodbye_expo + '\n\n' + travel_expo + '\n\n' + character_expo

        return {"exposition": exposition, "choices": choices}

    async def generate_image(self, story: Story, character: Character, recent_exposition: str) -> str:
        if character._base_image:
            # TODO: instead generate a new image based off of that one
            return character._base_image
        else:
            tools = load_tools(["dalle-image-generator"])
            prompt = PromptTemplate(
                input_variables=['input', 'tools',
                                 'tool_names', 'agent_scratchpad'],
                template=IMAGE_GENERATOR_PROMPT_TEMPLATE
            )
            agent = create_react_agent(self.llm, tools, prompt)
            agent_executor = AgentExecutor(agent=agent, tools=tools)
            response = await agent_executor.ainvoke({
                "input": character.public_description
            })
            return response['output']


async def main():
    llm = OpenAI(
        temperature=1,
        openai_api_key=os.environ.get('OPENAPI_API_KEY'),
        max_tokens=1024,
        model_name="gpt-3.5-turbo-instruct"
    )
    story = Story(**SAMPLE_STORY.model_dump())
    locations = SAMPLE_LOCATIONS
    characters = SAMPLE_CHARACTERS
    narrator = Narrator(llm=llm)
    story._db_obj = Object()

    first_location = Location(**locations[0].model_dump())
    first_location._db_obj = Object()

    third_location = Location(**locations[2].model_dump())
    third_location._db_obj = Object()

    first_character = Character(**characters[0].model_dump())
    first_character._db_obj = Object()
    first_character._db_obj.story = story
    first_character._db_obj.location = first_location
    first_character.green_room(llm=llm)

    third_character = Character(**characters[2].model_dump())
    third_character._db_obj = Object()
    third_character._db_obj.story = story
    third_character._db_obj.location = third_location
    third_character.green_room(llm=llm)

    story._db_obj.starting_location = first_location
    first_location._db_obj.starting_character = first_character
    third_location._db_obj.starting_character = third_character

    player_name = 'Steve'

    response = await narrator.embark(player_name, story, first_location, first_character)
    print(response['exposition'] + '\n\n')
    print(response['choices'])
    print('-----------')

    choice = response['choices'][0]
    print(f"My choice: {choice}")
    print('-----------')

    response = await narrator.interact(first_character, choice)
    first_character._interactions.append(first_character._last_interaction)
    first_character._last_interaction = None
    print(response['exposition'])
    print(response['choices'])
    print('-----------')

    choice = response['choices'][0]
    print(f"My choice: {choice}")
    print('-----------')

    # Change all conversation bots (testing save from storage)
    new_narrator = Narrator(llm, memory_buffer=narrator.memory.buffer)
    first_character.green_room(
        llm=llm,
        memory_buffer=first_character._memory.buffer,
        recent_history=first_character._interactions
    )
    print('AI changed\n-----------')

    response = await new_narrator.interact(first_character, choice)
    first_character._interactions.append(first_character._last_interaction)
    first_character._last_interaction = None
    print(response['exposition'])
    print(response['choices'])
    print('-----------')

    response = await new_narrator.travel(player_name, first_character, third_location)
    print(response['exposition'])
    print(response['choices'])
    print('-----------')


if __name__ == "__main__":
    asyncio.run(main())
