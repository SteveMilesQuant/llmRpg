import os
from typing import List
from langchain.chains import ConversationChain
from langchain.prompts.prompt import PromptTemplate
from langchain.memory import ConversationSummaryMemory
from langchain_openai import OpenAI
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


class Narrator:
    def __init__(self, llm):
        self.llm = llm
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

    def embark(self, player_name: str, story: Story):
        location = story._db_obj.starting_location
        character = location._db_obj.starting_character

        response = self.expositioner.invoke({
            "input": f'My name is {player_name}. I am just starting this story as a traveler from outside the realm and I know nothing about this land. Summarize the following setting to me.\n\nSETTING: {story.setting}'
        })
        land_expo = response['response']

        response = self.expositioner.invoke({
            "input": f'I arrive at {location.name}. Summarize that location to me according to the following description.\n\n\{location.name}: {location.description}'
        })
        location_expo = response['response']

        response = self.expositioner.invoke({
            "input": f'I prepare to interact with {character.name}, whom I have not met. Summarize that person to me according to the following description.\n\n\{character.name}: {character.public_description}'
        })
        character_expo = response['response']

        choices = [
            f'''"Hello, my name is {player_name}. I'm just passing through this area, but I'm looking for opportunities to help people."''',
            f'''"Hello, my name is {player_name}. I'm just passing through this area, but I'm looking for opportunities to make money."'''
        ]

        return {"exposition": land_expo + '\n\n' + location_expo + '\n\n' + character_expo, "choices": choices}

    def interact(self, character: Character, interaction_desc: str):
        character_response = character.interact(interaction_desc)
        response = self.expositioner.invoke({
            "input": f'The following interaction just occurred. Please describe it to me. Quote {character.name}\'s response into your description. \n\nI said to {character.name}: {interaction_desc}\n\n{character.name}\'s response to me: {character_response}'
        })
        choices = character.offer(self.memory.buffer)
        return {"exposition": response['response'], "choices": choices}

    def travel(self, previous_character: Character, new_location: Location):
        previous_location = previous_character._db_obj.location
        new_character = new_location._db_obj.starting_character

        goodbye = '''"Sorry, but I feel I must move on now. It will be quite a while before I return. Goodbye.'''
        goodbye_response = previous_character.interact(goodbye)
        response = self.expositioner.invoke({
            "input": f'The following interaction just occurred. Please describe it to me. Quote {previous_character.name}\'s response into your description. \n\nI say to {previous_character.name}: {goodbye}\n\n{previous_character.name}\'s response to me: {goodbye_response}'
        })
        goodbye_expo = response['response']

        response = self.expositioner.invoke({
            "input": f'Summarize traveling along the road from {previous_location.name} to {new_location.name}. The new location is described below.\n\n{new_location.name}:{new_location.description}'
        })
        travel_expo = response['response']

        response = self.expositioner.invoke({
            "input": f'I prepare to interact with {new_character.name}, whom I have not met. Summarize that person to me according to the following description.\n\n\{new_character.name}: {new_character.public_description}'
        })
        character_expo = response['response']

        choices = [
            f'''"Hello, my name is {player_name}. I'm just passing through this area, but I'm looking for opportunities to help people."''',
            f'''"Hello, my name is {player_name}. I'm just passing through this area, but I'm looking for opportunities to make money."'''
        ]

        exposition = goodbye_expo + '\n\n' + travel_expo + '\n\n' + character_expo

        return {"exposition": exposition, "choices": choices}


if __name__ == "__main__":
    llm = OpenAI(
        temperature=1, openai_api_key=os.environ.get('OPENAPI_API_KEY'), max_tokens=1024)
    story = Story(**SAMPLE_STORY.model_dump())
    locations = SAMPLE_LOCATIONS
    characters = SAMPLE_CHARACTERS
    narrator = Narrator(llm=llm)
    story._db_obj = Object()

    first_location = Location(**locations[0].model_dump())
    first_location._db_obj = Object()

    third_location = Location(**locations[0].model_dump())
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

    response = narrator.embark(player_name, story)
    print(response['exposition'] + '\n\n')
    print(response['choices'])
    print('-----------')

    choice = response['choices'][0]
    print(f"My choice: {choice}")
    print('-----------')

    response = narrator.interact(first_character, choice)
    print(response['exposition'])
    print(response['choices'])
    print('-----------')

    choice = response['choices'][0]
    print(f"My choice: {choice}")
    print('-----------')

    response = narrator.interact(first_character, choice)
    print(response['exposition'])
    print(response['choices'])
    print('-----------')

    response = narrator.travel(first_character, third_location)
    print(response['exposition'])
    print(response['choices'])
    print('-----------')
    print(third_location)
