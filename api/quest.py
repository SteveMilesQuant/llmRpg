import aiohttp
import asyncio
import json
import os
from pydantic import BaseModel
from typing import List, Literal


class Quest(BaseModel):
    id: int
    watcher: str
    behavior: str
    target_count: int
    achieved_count: int
    acceptance_status: Literal["accepted", "rejected", "pending"]

    def __eq__(self, other):
        if other.id == self.id:
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
    expected_response: Quest | str


QUEST_TRACKER_DESCRIPTION = '''You are in charge of tracking a list of quests that AI characters have for the human player. The input you receive is an existing list of existing quests and an additional new interaction between the human player and the AI character.
    
Use the following steps to decide how to respond.

Step 1: First, if the new interaction impacts one of the current quests, respond with the id of the impacted quest. Otherwise, continue to Step 2.

Step 2: If the character is asking the human player to go on a quest respond with "NEW". Otherwise, continue to Step 3.

Step 3: Respond with "PASS".
'''

QUEST_QUERY_TEMPLATE = '''The human player, {player_name}, and the character, {character_name}, have had a new interaction. Please respond according to your thought process.

Current quest list: {quests}

New interaction: {new_interaction}

Previous conversation history:
------------------------------
{recent_interactions}
------------------------------
'''

NEW_QUEST_DESCRIPTION = '''You are responsible for generating new quests. The input you receive is an existing list of existing quests and an additional new interaction between the human player and the AI character. Generate a quest with the following properties.
    id: unique integer identifier; pick a new id not in current quest list
    watcher: the name of the character
    behavior: the behavior requested of the human player
    target_count: the number of times the behavior should be observed
    achieved_count: the number of times the requested behavior has been observed
    acceptance_status: "pending"
'''

UPDATE_QUEST_DESCRIPTION = '''You are responsible for updating existing quests. The input you receive is an existing list of existing quests and an additional new interaction between the human player and the AI character. Update the quest with id={id}. You may update either the achieved_count or the acceptance status, but not both of them.
    achieved_count: The number of times the behavior has been observed or achieved. Increase this by one if the recent interaction demonstrates the observed behavior.
    acceptance_status: One of "accepted", "rejected", or "pending".
'''


QUEST_TRACKER_EXAMPLES: List[QuestTrackerExample] = [
    QuestTrackerExample(
        player_name="Dave",
        character_name="Penelope",
        new_interaction='''From Dave to Penelope: "Is there anything I can help you with?"\nFrom Penelope to Dave: "Yes, actually. I would like someone to deliver a letter to my sister."''',
        recent_interactions="",
        quests=[Quest(id=1, watcher="Joan", behavior="Kill orcs.", target_count=5,
                      achieved_count=3, acceptance_status="accepted"),
                Quest(id=2, watcher="Narrator", behavior="Travel to the north lands.", target_count=1,
                      achieved_count=0, acceptance_status="accepted")],
        expected_response="NEW"
    ),
    QuestTrackerExample(
        player_name="Jerry",
        character_name="Earl",
        new_interaction='''From Jerry to Earl: "Hello, my name is Jerry!"\nFrom Earl to Jerry: "Hi Jerry, what brings you here?"''',
        recent_interactions="",
        quests=[],
        expected_response="PASS"
    ),
    QuestTrackerExample(
        player_name="Dave",
        character_name="Penelope",
        new_interaction='''From Dave to Penelope: "How do you enjoy working in the city?"\nFrom Penelope to Dave: "It's good, actually. I love working in the hot sun."''',
        recent_interactions="",
        quests=[],
        expected_response="PASS"
    ),
    QuestTrackerExample(
        player_name="Karen",
        character_name="Narrator",
        new_interaction='''From Karen to Narrator:\nFrom Narrator to Karen: You deal a killing blow with your mighty axe to the orc standing in your way.''',
        recent_interactions="",
        quests=[Quest(id=1, watcher="Joan", behavior="Kill orcs.", target_count=5,
                      achieved_count=3, acceptance_status="accepted"),
                Quest(id=2, watcher="Narrator", behavior="Travel to the north lands.", target_count=1,
                      achieved_count=0, acceptance_status="accepted")],
        expected_response="1"
    ),
    QuestTrackerExample(
        player_name="Dave",
        character_name="Penelope",
        new_interaction='''From Dave to Penelope: "Sure, I can do that"\nFrom Penelope to Dave: "Thank you!"''',
        recent_interactions='''From Dave to Penelope: "Is there anything I can help you with?"\nFrom Penelope to Dave: "Yes, actually. I would like someone to deliver a letter to my sister."''',
        quests=[Quest(id=3, watcher="Penelope", behavior="Deliver a letter to Penelope's sister", target_count=1,
                      achieved_count=0, acceptance_status="pending")],
        expected_response="3"
    )
]


NEW_QUEST_EXAMPLES: List[QuestTrackerExample] = [
    QuestTrackerExample(
        player_name="Dave",
        character_name="Penelope",
        new_interaction='''From Dave to Penelope: Is there anything I can help you with?\nFrom Penelope to Dave: Yes, actually. I would like someone to deliver a letter to my sister.''',
        recent_interactions="",
        quests=[Quest(id=1, watcher="Joan", behavior="Kill orcs.", target_count=5,
                      achieved_count=3, acceptance_status="accepted"),
                Quest(id=2, watcher="Narrator", behavior="Travel to the north lands.", target_count=1,
                      achieved_count=0, acceptance_status="accepted")],
        expected_response=Quest(id=1, watcher="Penelope", behavior="Deliver a letter to Penelope's sister", target_count=1,
                                achieved_count=0, acceptance_status="pending")
    ),
    QuestTrackerExample(
        player_name="Jerry",
        character_name="Earl",
        new_interaction='''From Jerry to Earl: Is there anything I can do for you?\nFrom Earl to Jerry: I need you to kill some local orcs. I believe there are five of them.''',
        recent_interactions="",
        quests=[],
        expected_response=Quest(id=1, watcher="nEarl", behavior="Kill orcs", target_count=5,
                                achieved_count=0, acceptance_status="pending")
    )
]

UPDATE_QUEST_EXAMPLES: List[QuestTrackerExample] = [
    QuestTrackerExample(
        player_name="Dave",
        character_name="Penelope",
        new_interaction='''From Dave to Penelope: "Sure, I can do that"\nFrom Penelope to Dave: "Thank you!"''',
        recent_interactions='''From Dave to Penelope: "Is there anything I can help you with?"\nFrom Penelope to Dave: "Yes, actually. I would like someone to deliver a letter to my sister."''',
        quests=[Quest(id=1, watcher="Penelope", behavior="Deliver a letter to Penelope's sister", target_count=1,
                      achieved_count=0, acceptance_status="pending")],
        expected_response=Quest(id=1, watcher="Penelope", behavior="Deliver a letter to Penelope's sister", target_count=1,
                                achieved_count=0, acceptance_status="accepted")
    ),
    QuestTrackerExample(
        player_name="Dave",
        character_name="Penelope",
        new_interaction='''From Dave to Penelope: "I'm sorry, but I can't do that for you."\nFrom Penelope to Dave: "That's ok. I understand"''',
        recent_interactions='''From Dave to Penelope: "Is there anything I can help you with?"\nFrom Penelope to Dave: "Yes, actually. I would like someone to deliver a letter to my sister."''',
        quests=[Quest(id=1, watcher="Penelope", behavior="Deliver a letter to Penelope's sister", target_count=1,
                      achieved_count=0, acceptance_status="pending")],
        expected_response=Quest(id=1, watcher="Penelope", behavior="Deliver a letter to Penelope's sister", target_count=1,
                                achieved_count=0, acceptance_status="rejected")
    ),
    QuestTrackerExample(
        player_name="Dave",
        character_name="Annie",
        new_interaction='''From Dave to Annie: "I have a letter from your sister, Penelope." Hands her the letter.\nAnnie: "Thank you so much. Here is 20 gold."''',
        recent_interactions="",
        quests=[Quest(id=1, watcher="Penelope", behavior="Deliver a letter to Penelope's sister", target_count=1,
                      achieved_count=0, acceptance_status="accepted")],
        expected_response=Quest(id=1, watcher="Penelope", behavior="Deliver a letter to Penelope's sister", target_count=1,
                                achieved_count=1, acceptance_status="accepted")
    ),
    QuestTrackerExample(
        player_name="Jerry",
        character_name="Earl",
        new_interaction="From Earl to Narrotor:\nFrom Narrator to Earl: You killed an Orc.",
        recent_interactions="",
        quests=[Quest(id=3, watcher="Joan", behavior="Kill orcs.", target_count=5,
                      achieved_count=3, acceptance_status="accepted"),
                Quest(id=5, watcher="Narrator", behavior="Travel to the north lands.", target_count=1,
                      achieved_count=0, acceptance_status="accepted")],
        expected_response=Quest(id=3, watcher="Joan", behavior="Kill orcs.", target_count=5,
                                achieved_count=4, acceptance_status="accepted")
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

    async def update_quests(self, openai_http_session: aiohttp.ClientSession, player_name: str, character_name: str, interactions: List[tuple[str, str]] = []) -> None:
        recent_interactions = [interaction_to_string(
            player_name, i[0], character_name, i[1]) for i in interactions]
        recent_interactions_str = '\n'.join(recent_interactions)
        new_interaction = recent_interactions.pop()

        messages = [{"role": "system", "content": QUEST_TRACKER_DESCRIPTION}]
        messages = messages + TRACKER_FEW_SHOT_MESSAGES
        query = QUEST_QUERY_TEMPLATE.format(
            player_name=player_name,
            character_name=character_name,
            recent_interactions=recent_interactions_str,
            new_interaction=new_interaction,
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
            messages = [
                {"role": "system", "content": NEW_QUEST_DESCRIPTION}]
            messages = messages + NEW_QUEST_FEW_SHOT_MESSAGES
            messages = messages + [{"role": "user", "content": query}]
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
            messages = [{
                "role": "system",
                "content": UPDATE_QUEST_DESCRIPTION.format(id=int(action_json))
            }]
            messages = messages + UPDATE_QUEST_FEW_SHOT_MESSAGES
            messages = messages + [{"role": "user", "content": query}]
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
                self.quests[self.quests.index(new_quest)] = new_quest
            except:
                pass
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
            recent_interactions.append(interaction)
            await tracker.update_quests(
                openai_http_session,
                player_name=player_name,
                character_name=character_name,
                interactions=recent_interactions
            )
            print('')


if __name__ == "__main__":
    asyncio.run(main())
