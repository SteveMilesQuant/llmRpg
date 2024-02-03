import os
from ast import literal_eval
from typing import List
from langchain.chains import ConversationChain
from langchain.prompts.prompt import PromptTemplate
from langchain.memory import ConversationSummaryMemory
from langchain_openai import OpenAI
from datamodels import SAMPLE_CHARACTERS, SAMPLE_LOCATIONS, SAMPLE_STORY, LocationData, CharacterData
from character import Character

EXPOSITION_PREFIX = '''You are the narrator of an interactive story. The input you receive is from a Player playing as the main character of this story. Your response should describe what the Player sees and hears, and should use descriptive or creative language. The setting, locations, and characters in this story are described below.'''

OFFER_PREFIX = '''You are a helper to the narrator of an interactive story. Your response should be four choices that you offer the Player. The choices can be things the player can say to the character they're interacting with, which should be encapsulated in double quotes, and/or things the player can do in that moment, which would not be in double quotes. Offer the Player choices that are appropriate to the situation and character they are interacting with.  The setting, locations, and characters in this story are described below.

You MUST format your response as a Python array of strings, using three single quotes before and after each choice, to encapsulate each of the four choices you offer the Player. For example,
[
   \'''Hug them.\''',
   \'''"Tell them you're here to help."\''',
   \'''Stay silent and look awkardly to the side.\''',
   \'''"I don't think I can help you, sorry."\''',
]'''

COMMMON_SUFFIX = '''

Previous conversation history:
{history}

New input: {input}

Response:
'''


class Narrator:
    def __init__(self, llm, story_setting: str, locations: List[LocationData], characters: List[CharacterData]):
        self.llm = llm

        setting_desc = 'SETTING:\n----------\n' + story_setting + '\n----------\n\n'
        locations_desc = 'LOCATIONS:\n----------\n'
        for location in locations:
            locations_desc = locations_desc + location.name + \
                ': ' + location.description + '\n\n'
        locations_desc = locations_desc + '\n----------\n\n'

        characters_desc = 'CHARACTERS:\n----------\n'
        for character in characters:
            characters_desc = characters_desc + character.name + \
                ': ' + character.description + '\n\n'
        characters_desc = characters_desc + '\n----------\n\n'

        self.memory = ConversationSummaryMemory(llm=llm)

        exposition_template = EXPOSITION_PREFIX + setting_desc + \
            locations_desc + characters_desc + COMMMON_SUFFIX
        exposition_prompt = PromptTemplate(
            input_variables=['history', 'input'],
            template=exposition_template
        )
        self.exposition = ConversationChain(
            llm=llm,
            prompt=exposition_prompt,
            memory=self.memory
        )

        offer_template = OFFER_PREFIX + setting_desc + \
            locations_desc + characters_desc + COMMMON_SUFFIX
        offer_prompt = PromptTemplate(
            input_variables=['history', 'input'],
            template=offer_template
        )
        self.offerer = ConversationChain(
            llm=llm,
            prompt=offer_prompt,
            memory=self.memory
        )

    def offer(self):
        choices_str = self.offerer.predict(input="Offer me choices.")
        try:
            choices = literal_eval(choices_str)
        except:
            choices_str = self.offerer.predict(
                input="Your response was not formatted correctly. Please reformat.")
            choices = literal_eval(choices_str)
        return choices

    def embark(self, player_name: str, location_name: str, character_name: str):
        response = self.exposition.predict(
            input=f'My name is {player_name}. I am just starting this story as a traveler from outside the realm and I know nothing about this land. I have arrived in {location_name} and plan to initiate a conversation with {character_name}. Set the scene in three short paragraphs. In the first paragraph, describe the general setting of this story. In the second paragraph, describe the particular location I am in. In the third paragraph, describe the character I plan to talk to.')
        choices = self.offer()
        return {"exposition": response, "choices": choices}

    def interact(self, character: Character, interaction_desc: str):
        character_response = character.interact(interaction_desc)
        response = self.exposition.predict(
            input=f'The following interaction just happened. Please describe it to me. Weave the character\'s response into your description, quoting their response in double quotes. \n\nFrom me to {character.name}:{interaction_desc}\n\nFrom {character.name} to me:{character_response}')
        choices = self.offer()
        return {"exposition": response, "choices": choices}

    def travel(self, previous_location_name: str, previous_character: Character, new_location_name: str, new_character_name: str):
        goodbye = self.exposition.predict(
            input=f'Formulate a response for me to leave my conversation with {previous_character.name}')
        goodbye_response = previous_character.interact(goodbye)
        response = self.exposition.predict(
            input=f'The following interaction just happened. Please describe it to me. Weave the {previous_character.name}\'s response into your description, quoting their response in double quotes. \n\nFrom me to {previous_character.name}:{goodbye}\n\nFrom {previous_character.name} to me:{goodbye_response}\n\n My action: I traveled along the road from {previous_location_name} to {new_location_name}. I\'m preparing to interact with {new_character_name}, whom you should describe to me.')
        choices = self.offer()
        return {"exposition": response, "choices": choices}


if __name__ == "__main__":
    llm = OpenAI(
        temperature=1, openai_api_key=os.environ.get('OPENAPI_API_KEY'), max_tokens=1024)
    story = SAMPLE_STORY
    locations = SAMPLE_LOCATIONS
    characters = SAMPLE_CHARACTERS
    narrator = Narrator(llm=llm, story_setting=story.setting,
                        locations=locations, characters=characters)
    first_char_raw = characters[0]
    first_character = Character(
        **first_char_raw.model_dump(), llm=llm, story_setting=story.setting, locations=locations)

    third_char_raw = characters[2]
    third_character = Character(
        **third_char_raw.model_dump(), llm=llm, story_setting=story.setting, locations=locations)

    player_name = 'Steve'

    response = narrator.embark(
        player_name, locations[0].name, characters[0].name)
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

    response = narrator.travel(
        locations[0].name, first_character, locations[2].name, third_character.name)
    print(response['exposition'])
    print(response['choices'])
    print('-----------')
