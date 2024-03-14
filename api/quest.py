import aiohttp
import asyncio
import json
import os
from pydantic import BaseModel
from typing import List
from db import CharacterRecentHistoryDb


class Quest(BaseModel):
    id: int
    issuer: str
    target_behavior: str
    target_count: int
    achieved_count: int
    accepted: bool

    def __eq__(self, other):
        if isinstance(other, int):
            if self.id == other:
                return True
        elif other.id == self.id:
            return True
        return False

    def __str__(self) -> str:
        return self.model_dump_json()

    def __repr__(self) -> str:
        return self.model_dump_json()


class QuestTrackerExample(BaseModel):
    player_name: str
    character_name: str
    new_interaction: str
    recent_interactions: str
    quests: List[Quest]
    quest_id: str
    expected_response: Quest | str


QUEST_TRACKER_DESCRIPTION = '''You are in charge of tracking a list of quests that AI characters have for the human player. The input you receive is an existing list of existing quests and an additional new interaction between the human player and the AI character.
    
Use the following steps to decide how to respond.

Step 1: First, if the human player is accepting one of the unaccepted quests in the new interaction, respond with the id of the newly-accepted quest. Otherwise, continue to Step 2.

Step 2: If the human player is demonstrating the target behavior of one of the accepted quests in the new interaction, respond with the id of that quest. Otherwise, continue to Step 3.

Step 3: If the character is asking the human player to go on a quest respond with "NEW". Otherwise, continue to Step 4.

Step 4: Respond with "PASS".
'''

QUEST_QUERY_TEMPLATE = '''The human player, {player_name}, and the character, {character_name}, have had a new interaction. Please respond according to your thought process.

{quest_id}

Current quest list:
------------------------------
{quests}
------------------------------

Previous interactions:
------------------------------
{recent_interactions}
------------------------------

New interaction:
------------------------------
{new_interaction}
------------------------------
'''

NEW_QUEST_DESCRIPTION = '''You are responsible for generating new quests. The input you receive is an existing list of existing quests and an additional new interaction between the human player and the AI character. Generate a quest with the following properties.
    id: quest id, as provided in the input
    issuer: the name of the character
    target_behavior: the behavior requested of the human player
    target_count: the number of times the behavior should be observed
    achieved_count: 0
    accepted: false
'''

UPDATE_QUEST_DESCRIPTION = '''You are responsible for updating a quest. The input you receive is an existing list of existing quests and an additional new interaction between the human player and the AI character.

Use the following steps to decide how to respond.

Step 1: First, if the new interaction entails the human player accepting the quest, respond with "ACCEPTED". Otherwise, proceed to step 2.

Step 2: Respond with "ACHIEVED".
'''


QUEST_TRACKER_EXAMPLES: List[QuestTrackerExample] = [
    QuestTrackerExample(
        player_name="Dave",
        character_name="Penelope",
        new_interaction='''From Dave to Penelope: "Hello, my name is Dave."\nFrom Penelope to Dave: "Hi Dave. I'm penelope."''',
        recent_interactions="",
        quests=[],
        quest_id="",
        expected_response="PASS"
    ),
    QuestTrackerExample(
        player_name="Dave",
        character_name="Penelope",
        new_interaction='''From Dave to Penelope: "Is there anything I can help you with?"\nFrom Penelope to Dave: "Yes, actually. I would like someone to deliver a letter to my sister."''',
        recent_interactions="",
        quests=[],
        quest_id="",
        expected_response="NEW"
    ),
    QuestTrackerExample(
        player_name="Dave",
        character_name="Penelope",
        new_interaction='''From Dave to Penelope: "Sure, I can do that"\nFrom Penelope to Dave: "Thank you!"''',
        recent_interactions='''From Dave to Penelope: "Is there anything I can help you with?"\nFrom Penelope to Dave: "Yes, actually. I would like someone to deliver a letter to my sister."''',
        quests=[Quest(id=1, issuer="Penelope", target_behavior="Deliver a letter to Penelope's sister", target_count=1,
                      achieved_count=0, accepted=False)],
        quest_id="",
        expected_response="1"
    ),
    QuestTrackerExample(
        player_name="Dave",
        character_name="Penelope",
        new_interaction='''From Dave to Penelope: "I'm sorry, but I can't do that right now."\nFrom Penelope to Dave: "That's ok. I understand you're busy."''',
        recent_interactions='''From Dave to Penelope: "Is there anything I can help you with?"\nFrom Penelope to Dave: "Yes, actually. I would like someone to deliver a letter to my sister."''',
        quests=[Quest(id=1, issuer="Penelope", target_behavior="Deliver a letter to Penelope's sister", target_count=1,
                      achieved_count=0, accepted=False)],
        quest_id="",
        expected_response="PASS"
    ),
    QuestTrackerExample(
        player_name="Dave",
        character_name="Annie",
        new_interaction='''From Dave to Annie: "I have a letter from your sister, Penelope." Hands her the letter.\nAnnie: "Thank you so much. Here is 20 gold."''',
        recent_interactions="",
        quests=[Quest(id=1, issuer="Penelope", target_behavior="Deliver a letter to Penelope's sister", target_count=1,
                      achieved_count=0, accepted=False)],
        quest_id="",
        expected_response="1"
    ),
]


NEW_QUEST_EXAMPLES: List[QuestTrackerExample] = [
    QuestTrackerExample(
        player_name="Dave",
        character_name="Penelope",
        new_interaction='''From Dave to Penelope: "Is there anything I can help you with?"\nFrom Penelope to Dave: "Yes, actually. I would like someone to deliver a letter to my sister."''',
        recent_interactions="",
        quests=[],
        quest_id="Quest id: 7",
        expected_response=Quest(id=7, issuer="Penelope", target_behavior="Deliver a letter to Penelope's sister", target_count=1,
                                achieved_count=0, accepted=False)
    ),
    QuestTrackerExample(
        player_name="Jerry",
        character_name="Earl",
        new_interaction='''From Jerry to Earl: "Is there anything I can do for you?"\nFrom Earl to Jerry: "I need you to kill some local orcs. I believe there are five of them."''',
        recent_interactions="",
        quests=[],
        quest_id="Quest id: 3",
        expected_response=Quest(id=3, issuer="Earl", target_behavior="Kill orcs", target_count=5,
                                achieved_count=0, accepted=False)
    )
]

UPDATE_QUEST_EXAMPLES: List[QuestTrackerExample] = [
    QuestTrackerExample(
        player_name="Dave",
        character_name="Penelope",
        new_interaction='''From Dave to Penelope: "Sure, I can do that"\nFrom Penelope to Dave: "Thank you!"''',
        recent_interactions='''From Dave to Penelope: "Is there anything I can help you with?"\nFrom Penelope to Dave: "Yes, actually. I would like someone to deliver a letter to my sister."''',
        quests=[Quest(id=1, issuer="Penelope", target_behavior="Deliver a letter to Penelope's sister", target_count=1,
                      achieved_count=0, accepted=False)],
        quest_id="Quest id: 1",
        expected_response="ACCEPTED"
    ),
    QuestTrackerExample(
        player_name="Dave",
        character_name="Annie",
        new_interaction='''From Dave to Annie: "I have a letter from your sister, Penelope." Hands her the letter.\nAnnie: "Thank you so much. Here is 20 gold."''',
        recent_interactions="",
        quests=[Quest(id=3, issuer="Penelope", target_behavior="Deliver a letter to Penelope's sister", target_count=1,
                      achieved_count=0, accepted=True)],
        quest_id="Quest id: 3",
        expected_response="ACHIEVED"
    ),
    QuestTrackerExample(
        player_name="Jerry",
        character_name="Narrator",
        new_interaction="From Earl to Narrator:\nFrom Narrator to Earl: You killed an Orc.",
        recent_interactions="",
        quests=[Quest(id=8, issuer="Joan", target_behavior="Kill orcs.", target_count=5,
                      achieved_count=3, accepted=True)],
        quest_id="Quest id: 8",
        expected_response="ACHIEVED"
    )
]

TRACKER_FEW_SHOT_MESSAGES = []
for example in QUEST_TRACKER_EXAMPLES:
    query = QUEST_QUERY_TEMPLATE.format(**example.model_dump())
    TRACKER_FEW_SHOT_MESSAGES.append({"role": "user", "content": query})
    TRACKER_FEW_SHOT_MESSAGES.append(
        {"role": "assistant", "content": f'{example.expected_response}'})

NEW_QUEST_FEW_SHOT_MESSAGES = []
for example in NEW_QUEST_EXAMPLES:
    query = QUEST_QUERY_TEMPLATE.format(**example.model_dump())
    NEW_QUEST_FEW_SHOT_MESSAGES.append({"role": "user", "content": query})
    NEW_QUEST_FEW_SHOT_MESSAGES.append(
        {"role": "assistant", "content": f'{example.expected_response}'})

UPDATE_QUEST_FEW_SHOT_MESSAGES = []
for example in UPDATE_QUEST_EXAMPLES:
    query = QUEST_QUERY_TEMPLATE.format(**example.model_dump())
    UPDATE_QUEST_FEW_SHOT_MESSAGES.append({"role": "user", "content": query})
    UPDATE_QUEST_FEW_SHOT_MESSAGES.append(
        {"role": "assistant", "content": f'{example.expected_response}'})


def interaction_to_string(player_name: str, player_to_character: str, character_name: str, character_to_user: str):
    return f'''From {player_name} to {character_name}: {player_to_character}\nFrom {character_name} to {player_name}: {character_to_user}'''


class QuestTracker(BaseModel):
    chat_url: str
    chat_model: str
    quests: List[Quest] = []
    verbose: bool = False

    async def update_quests(self, openai_http_session: aiohttp.ClientSession, player_name: str, character_name: str, interactions: List[CharacterRecentHistoryDb] = []) -> None:
        recent_interactions = [interaction_to_string(
            player_name, i.user_input, character_name, i.character_response) for i in interactions]
        recent_interactions_str = '\n'.join(recent_interactions)
        new_interaction = recent_interactions.pop()

        messages = [{"role": "system", "content": QUEST_TRACKER_DESCRIPTION}]
        messages = messages + TRACKER_FEW_SHOT_MESSAGES
        query = QUEST_QUERY_TEMPLATE.format(
            player_name=player_name,
            character_name=character_name,
            recent_interactions=recent_interactions_str,
            new_interaction=new_interaction,
            quest_id="",
            quests=self.quests
        )
        messages = messages + [{"role": "user", "content": query}]
        response = await openai_http_session.post(
            url=self.chat_url,
            json={
                "model": self.chat_model,
                "messages": messages,
                "temperature": 0
            })
        response_json = await response.json()
        action_json = response_json['choices'][0]['message']['content'].strip()
        if action_json == "PASS":
            pass
        elif action_json == "NEW":
            new_id = max([q.id for q in self.quests], default=1)
            query_new = QUEST_QUERY_TEMPLATE.format(
                player_name=player_name,
                character_name=character_name,
                recent_interactions=recent_interactions_str,
                new_interaction=new_interaction,
                quest_id=f"Quest id: {new_id}",
                quests=[]
            )

            messages = [{"role": "system", "content": NEW_QUEST_DESCRIPTION}]
            messages = messages + NEW_QUEST_FEW_SHOT_MESSAGES
            messages = messages + [{"role": "user", "content": query_new}]
            response = await openai_http_session.post(
                url=self.chat_url,
                json={
                    "model": self.chat_model,
                    "messages": messages,
                    "temperature": 0
                })
            response_json = await response.json()
            response_msg = response_json['choices'][0]['message']
            quest_json = response_msg['content'].strip()
            try:
                new_quest = Quest(**json.loads(quest_json))
                self.quests.append(new_quest)
            except:
                pass
        else:
            target_id = int(action_json)
            quest = self.quests[self.quests.index(target_id)]

            query_update = QUEST_QUERY_TEMPLATE.format(
                player_name=player_name,
                character_name=character_name,
                recent_interactions=recent_interactions_str,
                new_interaction=new_interaction,
                quest_id=f"Quest id: {target_id}",
                quests=[quest]
            )

            messages = [
                {"role": "system", "content": UPDATE_QUEST_DESCRIPTION}]
            messages = messages + UPDATE_QUEST_FEW_SHOT_MESSAGES
            messages = messages + [{"role": "user", "content": query_update}]
            response = await openai_http_session.post(
                url=self.chat_url,
                json={
                    "model": self.chat_model,
                    "messages": messages,
                    "temperature": 0
                })
            response_json = await response.json()
            response_msg = response_json['choices'][0]['message']
            update_json = response_msg['content'].strip()
            if update_json == 'ACCEPTED':
                quest.accepted = True
            else:
                quest.achieved_count = quest.achieved_count + 1

        if self.verbose:
            print(f"Quest action: {action_json}")
            print("Quests:")
            for quest in self.quests:
                print(f"\t{quest}")


async def main():
    verbose = True

    # HTTP configuration
    chat_url = "https://api.openai.com/v1/chat/completions"
    chat_model = "gpt-3.5-turbo"
    headers = {
        'content-type': 'application/json',
        'authorization': f'Bearer {os.environ.get("OPENAI_API_KEY")}'
    }

    tracker = QuestTracker(
        chat_url=chat_url, chat_model=chat_model, verbose=verbose)

    player_name = 'Steve'
    character_name = 'Cheryl'

    interactions = [
        ('''"Hello!''', '''"Hello there! Welcome to my humble farm in Southumbra. My name is Cheryl. What brings you to these parts?"'''),
        ('''"I'm just passing through. Is there anything I can help you with?"''',
         '''"Yes, I'm concerned about the blight affecting farms to the North of me, but I can't leave my farm. Would you investigate for me?"'''),
        ('''"Yes, of course."''', '''"Thank you."'''),
        ('''"I know you've been causing the blight with your chemical side-product. I saw your men dumping those chemicals into the water."''',
         '''"If the cat's out of the bag, I can't just let you leave here alive."'''),
    ]

    recent_interactions = []

    async with aiohttp.ClientSession(headers=headers) as openai_http_session:
        for index, interaction in enumerate(interactions):
            if index == 3:
                character_name = 'Daryl'
                recent_interactions = []
            print(interaction_to_string(player_name,
                  interaction[0], character_name, interaction[1]))
            recent_interactions.append(CharacterRecentHistoryDb(
                character_session_id=1,
                sort_index=index,
                user_input=interaction[0],
                character_response=interaction[1]
            ))
            await tracker.update_quests(
                openai_http_session,
                player_name=player_name,
                character_name=character_name,
                interactions=recent_interactions
            )
            print('')


if __name__ == "__main__":
    asyncio.run(main())
