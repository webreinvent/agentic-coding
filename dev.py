from autogen_agentchat.base import TaskResult
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.agents import CodeExecutorAgent, AssistantAgent
from autogen_ext.code_executors.docker import DockerCommandLineCodeExecutor
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import TextMentionTermination
from config import config
import asyncio

async def main():

    model = OpenAIChatCompletionClient(
        model="gpt-3.5-turbo",
        api_key=config["openai"]["api_key"],
    )


    code_developer_agent = AssistantAgent(
        name="CodeDeveloper",
        model_client=model,
        system_message="You are a Python, Laravel, Vue, Nuxt code developer agent working with Autogen Code Executor Agent."
        +" You should always write code in code block and specify the language."
        +" You should write once block at a time and then pass it on to Autogen Code Executor Agent. "
        +" Once Autogen Code Executor Agent executes the code and you have the result, then explain the result and then you can write another block."
        +" Once the all code blocks are executed then exactly say 'TERMINATE'"
    )

    docker_executor = DockerCommandLineCodeExecutor(
        work_dir="/tmp/autogen",
    )

    code_executor_agent = CodeExecutorAgent(
        name="CodeExecutor",
        code_executor=docker_executor,
    )

    await docker_executor.start()

    team = RoundRobinGroupChat(
        [code_developer_agent, code_executor_agent],
        termination_condition=TextMentionTermination("TERMINATE"),
        max_turns=10
    )

    task = "How to fetch data from in python 'https://dummyjson.com/test' and print the result in a formatted way."

    async for message in team.run_stream(task=task):
        if isinstance(message, TaskResult):
            print(f"Stopping Reason: {message.stop_reason}")
        else:
            print(f"{message.source}: {message.content}")

    print("Done")

    await docker_executor.stop()

if __name__ == "__main__":
    asyncio.run(main())

