from autogen_ext.models.openai import OpenAIChatCompletionClient
from config import config
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.ui import Console

import asyncio

async def main():
    print(config["openai"]["api_key"])
    model = OpenAIChatCompletionClient(
        model="gpt-3.5-turbo",
        api_key=config["openai"]["api_key"],
    )

    topic = "Rise of Artificial Intelligence"
    support_agent = AssistantAgent(
        name="SupportAgent",
        model_client=model,
        system_message="You are a support agent specialized for the topic " + topic + ". Provide detailed and accurate information.",
    )

    critic_agent = AssistantAgent(
        name="CriticAgent",
        model_client=model,
        system_message="You are a critic agent specialized for the topic " + topic + ". Provide critical and constructive feedback.",
    )
    termination = TextMentionTermination("TERMINATE")
    group_chat = RoundRobinGroupChat(
        [support_agent, critic_agent],
        termination_condition=termination,
    )

    await Console(group_chat.run_stream(task="Debate on AI"));



if __name__ == "__main__":
    asyncio.run(main())