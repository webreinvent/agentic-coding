from autogen_agentchat.agents import CodeExecutorAgent
from autogen_ext.code_executors.docker import DockerCommandLineCodeExecutor
from autogen_agentchat.messages import TextMessage
from autogen_core import CancellationToken
import asyncio

async def main():
    docker_executor = DockerCommandLineCodeExecutor(
        work_dir="/tmp/autogen",
    )

    await docker_executor.start()

    code_executor = CodeExecutorAgent(
        name="CodeExecutor",
        code_executor=docker_executor,
    )

    code = """```python
print("Hello, World!");
```"""
    res = await code_executor.on_messages(
        messages=[TextMessage(content=code, source="user")],
        cancellation_token=CancellationToken(),
    )

    print(res)

    await docker_executor.stop()

if __name__ == "__main__":
    asyncio.run(main())

