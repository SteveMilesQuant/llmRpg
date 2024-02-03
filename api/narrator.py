import os
from ast import literal_eval
from typing import List
from langchain.chains import ConversationChain
from langchain.prompts.prompt import PromptTemplate
from langchain.memory import ConversationSummaryMemory
from langchain_openai import OpenAI
from datamodels import Object, SAMPLE_CHARACTERS, SAMPLE_LOCATIONS, SAMPLE_STORY
from story import Story
from location import Location
from character import Character


EXPOSITION_PREFIX = '''You are the narrator of an interactive story. The input you receive is from a Player playing as the main character of this story. Your response should describe what the Player sees and hears, and should use descriptive or creative language, but should generally be brief (2-5 sentences).'''

DIALOG_PREFIX = '''You are a helper to the narrator of an interactive story. Your response should be dialog generated for the user that is appropriate for the current situation.'''

OFFER_PREFIX = '''You are a helper to the narrator of an interactive story. Your response should be four choices that you offer the Player. The choices can be things the player can say to the character they're interacting with, which should be encapsulated in double quotes, and/or things the player can do in that moment, which would not be in double quotes. Offer the Player choices that are appropriate to the situation and character they are interacting with.

You MUST format your response as a Python array of strings, using three single quotes before and after each choice, to encapsulate each of the four choices you offer the Player. For example,
[
   \'''First choice\''',
   \'''Second choice with "dialog in double quotes"\''',
   etc.
]'''

COMMMON_SUFFIX = '''

Previous conversation history:
{history}

New input: {input}

Response:
'''


class Narrator:
    def __init__(self, llm):
        self.llm = llm
        self.memory = ConversationSummaryMemory(llm=llm)

        exposition_template = EXPOSITION_PREFIX + COMMMON_SUFFIX
        exposition_prompt = PromptTemplate(
            input_variables=['history', 'input'],
            template=exposition_template
        )
        self.expositioner = ConversationChain(
            llm=llm,
            prompt=exposition_prompt,
            memory=self.memory
        )

        dialogue_template = DIALOG_PREFIX + COMMMON_SUFFIX
        dialog_prompt = PromptTemplate(
            input_variables=['history', 'input'],
            template=dialogue_template
        )
        self.dialoguer = ConversationChain(
            llm=llm,
            prompt=dialog_prompt,
            memory=self.memory
        )

        offer_template = OFFER_PREFIX + COMMMON_SUFFIX
        offer_prompt = PromptTemplate(
            input_variables=['history', 'input'],
            template=offer_template
        )
        self.offerer = ConversationChain(
            llm=llm,
            prompt=offer_prompt,
            memory=self.memory
        )

    def offer(self, whatfor: str):
        choices_str = self.offerer.predict(
            input=f"Offer me choices for {whatfor}.")
        try:
            choices = literal_eval(choices_str)
        except:
            choices_str = self.offerer.predict(
                input="Your response was not formatted correctly. Please reformat.")
            choices = literal_eval(choices_str)
        return choices

    def embark(self, player_name: str, story: Story):
        location = story._db_obj.starting_location
        character = location._db_obj.starting_character

        land_expo = self.expositioner.predict(
            input=f'My name is {player_name}. I am just starting this story as a traveler from outside the realm and I know nothing about this land. Summarize the following setting to me.\n\nSETTING: {story.setting}')
        location_expo = self.expositioner.predict(
            input=f'I arrive at {location.name}. Summarize that location to me according to the following description.\n\n\{location.name}: {location.description}')
        character_expo = self.expositioner.predict(
            input=f'I prepare to interact with {character.name}, whom I have not met. Summarize that person to me according to the following description.\n\n\{character.name}: {character.description}')
        choices = self.offer(f"introducing myself to {character.name}")
        return {"exposition": land_expo + '\n\n' + location_expo + '\n\n' + character_expo, "choices": choices}

    def interact(self, character: Character, interaction_desc: str):
        character_response = character.interact(interaction_desc)
        response = self.expositioner.predict(
            input=f'The following interaction just occurred. Please describe it to me. Quote {character.name}\'s response into your description. \n\nI say to {character.name}: {interaction_desc}\n\n{character.name}\'s response to me: {character_response}')
        choices = self.offer(f'responding to {character.name}')
        return {"exposition": response, "choices": choices}

    def travel(self, previous_character: Character, new_location: Location):
        previous_location = previous_character._db_obj.location
        new_character = new_location._db_obj.starting_character

        goodbye = self.dialoguer.predict(
            input=f'Formulate a response for me to leave my conversation with {previous_character.name}')
        goodbye_response = previous_character.interact(goodbye)
        goodbye_expo = self.expositioner.predict(
            input=f'The following interaction just occurred. Please describe it to me. Quote {previous_character.name}\'s response into your description. \n\nI say to {previous_character.name}: {goodbye}\n\n{previous_character.name}\'s response to me: {goodbye_response}')
        travel_expo = self.expositioner.predict(
            input=f'Summarize traveling along the road from {previous_location.name} to {new_location.name}. The new location is described below.\n\n{new_location.name}:{new_location.description}')
        character_expo = self.expositioner.predict(
            input=f'I prepare to interact with {new_character.name}, whom I have not met. Summarize that person to me according to the following description.\n\n\{new_character.name}: {new_character.description}')
        choices = self.offer(f"introducing myself to {new_character.name}")
        return {"exposition": goodbye_expo + '\n\n' + travel_expo + '\n\n' + character_expo, "choices": choices}


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

    response = narrator.travel(first_character, third_location)
    print(response['exposition'])
    print(response['choices'])
    print('-----------')
