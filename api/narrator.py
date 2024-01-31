from langchain.prompts.prompt import PromptTemplate
from langchain.agents import AgentExecutor, create_react_agent
from langchain.memory import ConversationBufferMemory

NARRATOR_PREFIX = '''
You are the narrator of an interactive story. The input you receive is from a Player playing as the main character of this story. Your responses should describe what the Player sees and hears, and should use descriptive or creative language. The setting of this story is described below, but you are welcome to embellish as you see fit.

If this is the first interaction you have with the Player, then you should set the scene for them by describing the general setting of the land they're in.

'''

NARRATOR_SUFFIX = '''

TOOLS:
------

You have access to the following tools, but should never need to use a tool:

{tools}

To use a tool, please use the following format:

```
Thought: Do I need to use a tool? Yes
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
```

When you have a response to say to the Player, or if you do not need to use a tool, you MUST use the format:

```
Thought: Do I need to use a tool? No
Final Answer: [your response here]
```

Begin!

Previous conversation history:
{chat_history}

New input: {input}
{agent_scratchpad}
'''


class Narrator:
    def __init__(self, llm, story_setting: str):
        self.llm = llm
        self.prompt = PromptTemplate(input_variables=[
                                     'agent_scratchpad', 'chat_history', 'input', 'tool_names', 'tools'], template=NARRATOR_PREFIX + 'Setting:' + story_setting + NARRATOR_SUFFIX)
        self.agent = create_react_agent(llm, [], self.prompt)
        self.memory = ConversationBufferMemory(memory_key="chat_history")
        self.agent_executor = AgentExecutor(
            agent=self.agent, tools=[], memory=self.memory, verbose=False)

    def query(self, query_input: str) -> str:
        response = self.agent_executor.invoke(
            {
                "input": query_input,
            }
        )
        return response['output']
