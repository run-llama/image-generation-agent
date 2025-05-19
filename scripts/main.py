import json
from app_frontend import gr, frontend
from workflow import workflow
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from pydantic import BaseModel
from llama_index.core.agent.workflow import ToolCall, ToolCallResult

app = FastAPI(default_response_class=ORJSONResponse)

class ApiInput(BaseModel):
    prompt: str

class ApiOutput(BaseModel):
    process: str
    response: str

@app.post("/agent")
async def run_agent(inpt: ApiInput) -> ApiOutput:
    handler = workflow.run(user_msg=inpt.prompt)
    process = ""
    async for event in handler.stream_events():
        if isinstance(event, ToolCallResult):
            process += f"Tool call result for **{event.tool_name}**:\n\n```json\n{event.tool_output.model_dump_json(indent=4)}\n```\n"
        elif isinstance(event, ToolCall):
            process += f"Calling tool **{event.tool_name}** with input args:\n\n```json\n{json.dumps(event.tool_kwargs, indent=4)}\n```\n"
    response = await handler
    response = str(response)
    return ApiOutput(process=process, response=response)

app = gr.mount_gradio_app(app, frontend, "")
