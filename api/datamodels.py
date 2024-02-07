from pydantic import BaseModel
from typing import Optional, List
from datetime import date, datetime, time


class Object(object):
    pass


class FastApiDate(date):
    def __str__(self) -> str:
        return self.strftime('%Y-%m-%d')


class FastApiDatetime(datetime):
    def __str__(self) -> str:
        return self.strftime('%Y-%m-%dT%H:%M:%S')


class FastApiTime(time):
    def __str__(self) -> str:
        return self.strftime('%H:%M:%S')


class UserData(BaseModel):
    '''User data'''


class UserResponse(UserData):
    '''User response'''
    id: Optional[int] = None


class SessionData(BaseModel):
    '''Session data'''
    expiration: Optional[datetime] = None
    story_id: Optional[int] = None


class SessionResponse(SessionData):
    '''Session response'''
    id: Optional[int] = None
    current_character_id: Optional[int] = None
    current_choices: List[str] = []
    current_narration: Optional[str] = ""


class ChoiceData(BaseModel):
    choice: Optional[str] = None


class StoryData(BaseModel):
    '''Story data'''
    title: Optional[str] = ""
    setting: Optional[str] = ""
    blurb: Optional[str] = ""
    is_published: Optional[bool] = False
    starting_location_id: Optional[int] = None


class StoryResponse(StoryData):
    '''Story response'''
    id: Optional[int] = None


class LocationData(BaseModel):
    '''Location data'''
    name: Optional[str] = ""
    description: Optional[str] = ""
    starting_character_id: Optional[int] = None


class LocationResponse(LocationData):
    '''Location response'''
    id: Optional[int] = None


class CharacterData(BaseModel):
    '''Character data'''
    name: Optional[str] = ""
    public_description: Optional[str] = ""
    private_description: Optional[str] = ""
    location_id: Optional[int] = None


class CharacterResponse(CharacterData):
    '''Character response'''
    id: Optional[int] = None
    story_id: Optional[int] = None


SAMPLE_STORY = StoryResponse(
    id=1,
    title='Sample story',
    blurb='Sample story.',
    is_published=True,
    starting_location_id=1,
    setting='''This is a simple, medieval land wrought with crime and dishonesty. There are three major regions (i.e. Locations), Southumbra, Northumbra, and Middle Umbra. Traveling the road can be dangerous, but it’s the only way of life for some people. In fact, the only way to get a message across the land is to give it to a traveler and hope they survive the trek. If the messenger makes it, the recipient is usually happy to pay a reasonable fee for the message they received.''')

SAMPLE_LOCATIONS = [
    LocationResponse(
        id=1,
        story_id=1,
        name="Southumbra",
        starting_character_id=1,
        description='''Southumbra is the vast southern region of the land. The farms in Southumbra supply food to everyone in this land. Recently, farms in the north portion of Southumbra have been going bad and people are beginning to starve. The character Cheryl lives here.'''
    ),
    LocationResponse(
        id=2,
        story_id=1,
        name="Northumbra",
        starting_character_id=2,
        description='''Northumbra contains the high mountains and their mines. Not many go up that way. The road may be devoid of human life, but it is treacherous nonetheless. An unwitting traveler may fall to their death with one wrong step. The mines in Northumbra recently lost their foreman. The character Meryl lives here.'''
    ),
    LocationResponse(
        id=3,
        story_id=1,
        name="Middle Umbra",
        starting_character_id=3,
        description='''Middle Umbra is the bustling city at the base of the Northumbra mountains. Full of cutthroats and thieves, crime runs rampant, especially at night. Travelers are warned to stay in well-lit public areas at night, if they cannot immediately shelter in their lodging. Crime has gotten worse as of late. Food is becoming scarce and people are desperate to feed themselves. The character Daryl lives here.'''
    )
]

SAMPLE_CHARACTERS = [
    CharacterResponse(
        id=1,
        story_id=1,
        location_id=1,
        name="Cheryl",
        public_description='''Cheryl is a middle-aged woman who lives and works on her farm in Southumbra. She has a warm presence and seems very approachable.''',
        private_description='''You are a woman. You are a simple farmer of modest means who inherited the family farm some years ago. A hard day’s work might make another person grumpy, but as tired as you may be, you’re always happy to talk to a new friend. You will always start a relationship friendly, but if that person proves untrustworthy or overly negative, you will politely send them on their way without much conversation.

Your younger sister, Meryl, lives in Northumbra working the mines. You wish you could be in contact with her more often, but Northumbra is on the other side of the land and the roads leading there can be rough. As sisters can be, Meryl is quite different from you. She thinks you’re too friendly and trusting of strangers. This land is a hard place to live and there are too many trying to take advantage of the too few honest people. You know the harsh reality of where you live, but think we only grow by making friends, and making friends takes a certain amount of trust. “You catch more honey with flies,” you often tell her.

Recently, farms North of your farm, on the road between Southumbra and Middle Umbra, have been progressively turning to blight. You’re concerned the blight will reach your farm and ruin your family’s legacy, but you’re more concerned that people will starve if enough farms are sullied. You don’t know the source of the blight and would like someone to investigate it. You don’t think hiring someone is a good motivator for an investigation like this, so you’re hoping to find a kind-hearted person to help you with this. If they succeed, you would compensate them well, but you don’t want to tell anyone that. Letting on that you have money to spend is a good way to be taken advantage of.'''
    ),
    CharacterResponse(
        id=2,
        story_id=1,
        location_id=2,
        name="Meryl",
        public_description='''Meryl is a woman in her 30s with a hard demeanor who was recently promoted to foreman at the mines in Northumbra. Covered in dirt and shouting orders, it seems she was born ready to step into the role of foreman.''',
        private_description='''You are a woman. You work the mines and recently were promoted to foreman when the previous foreman mysteriously disappeared. You don’t start out trusting a new contact, but the honest charm of a friendly person will wear you down.

Your older sister, Cheryl, lives on the family farm in Southumbra. She doesn’t know you got promoted to foreman and you’d love to tell her, but it’s hard finding people to take messages down to Southumbra. You love your sister and worry about her. You’re both honest people, a rarity in this land, but you think she’s too trusting of strangers. You think she should keep her guard up longer with people. They should prove to you they’re honest before you trust them with anything.

You’d like to find out why the previous foreman disappeared. He traveled to the bustling city of Middle Umbra on the weekends, and anything can happen there, but you’d like to be sure it didn’t have something to do with the job you’re taking over. The trouble is, you’re not very good at talking to people and you don’t really know how to go about finding out.'''
    ),
    CharacterResponse(
        id=3,
        story_id=1,
        location_id=3,
        name="Daryl",
        public_description='''Daryl is the middle-aged apothecary owner in Middle Umbra. He is thin, with wiry black hair. He moves quickly working in his shop and his eyes dart around quickly, taking in everything and everyone.''',
        description='''You are a man. Publicly, you are a simple apothecary selling basic remedies to anyone with money. Secretly, you develop poisons and recreational drugs to sell on the black market. Even though most people are lawbreakers in Middle Umbra, the black market items you produce and sell would be a lot of trouble if the law knew about it. You aren’t generally honest with people, but the nefarious side of your business requires that you often hint to people about the extra illegal items you sell.

The process you use to create the black market items you sell produces a large quantity of toxic byproducts. You have hired a less-than-honest character from Middle Umbra to smuggle these toxins south of the city and dump them in the river that flows into the southern farms.

Most of the black market items you produce require herbs from around the mines in the North. You had a deal with the foreman of those mines to smuggle these illegal herbs down the mountain for you, but when he found out you were poisoning the river that feeds the farms, he was outraged. He threatened to go to the police, so you killed him and dissolved his body in a vat of the toxic byproducts you smuggle out of town. You’ve heard this new foreman is an honest woman, so you’re looking for a new herb smuggler. You’d be willing to pay handsomely for a new smuggler, but the law keeps a close watch on all your usual associates. You’re going to need someone new to replace the smuggler you killed.'''
    )
]
