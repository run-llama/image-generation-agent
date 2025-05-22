# server.py
import json
import asyncio
import websockets
from workflow import workflow
from llama_index.core.agent.workflow.workflow_events import ToolCall, ToolCallResult

async def run_agent(websocket):
    async for prompt in websocket:
        handler = workflow.run(user_msg=prompt)
        async for event in handler.stream_events():
            if isinstance(event, ToolCallResult):
                await websocket.send(f"**Result from `{event.tool_name}`**:\n\n{event.tool_output.content}\n\n")
            elif isinstance(event, ToolCall):
                await websocket.send(f"### Calling tool: `{event.tool_name}`\n\n```json\n{json.dumps(event.tool_kwargs, indent=4)}\n```\n\n")
        response = await handler
        response = str(response)
        await websocket.send("### Final output\n\n" + response)
        await websocket.send("[END]")

async def main():
    print("Starting server on ws://localhost:8765")
    async with websockets.serve(run_agent, "localhost", 8765):
        await asyncio.Future()  # Run forever

if __name__ == "__main__":
    asyncio.run(main())
