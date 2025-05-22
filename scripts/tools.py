import base64
import json
from pathlib import Path
from utils import get_api_keys
from llama_index.llms.openai import OpenAIResponses
from typing import Literal
from pydantic import BaseModel, Field
from llama_index.llms.google_genai import GoogleGenAI
from llama_index.core.llms import ChatMessage, MessageRole, ImageBlock, TextBlock


class ImageEvaluation(BaseModel):
    faithfulness: int = Field(description="Faithfulness of the generated image to the generation prompt, from 0 to 100")
    quality: Literal["low", "mediocre", "average", "upper-intermediate", "high", "very high"] = Field(description="Quality of the image, expressed as one of: 'low', 'mediocre', 'average', 'upper-intermediate', 'high', 'very high'")
    prompt_agnostic_description: str = Field(description="Description of the image, agnostic of the image generation prompt")

openai_api_key, google_api_key =get_api_keys()
async_openai_client = OpenAIResponses(api_key=openai_api_key, model="gpt-4.1-mini",built_in_tools=[{"type": "image_generation"}])
llm = GoogleGenAI(model="gemini-2.0-flash", api_key=google_api_key)
llm_struct = llm.as_structured_llm(ImageEvaluation)

async def generate_image(prompt: str = Field(description="The image generation prompt")) -> str:
    """
    This tool useful to generate images.

    Args:
        prompt (str): The image generation prompt

    """
    try:
        messages = [ChatMessage.from_str(content=prompt, role="user")]
        img = await async_openai_client.achat(messages)
        for block in img.message.blocks:
            if isinstance(block, ImageBlock):
                image_bytes = base64.b64decode(block.image)
                with open("output.png", "wb") as f:
                    f.write(image_bytes)
        return "Image successfully generated"
    except Exception as e:
        return f"An error occurred during image generation: {e.__str__()}"

async def evaluate_generated_image(prompt: str = Field(description="The original prompt used to generate the image")) -> str:
    """
    This tool is useful to evaluate a generated image.

    Args:
        prompt (str): The original prompt used to generate the image

    """
    messages = [ChatMessage(role=MessageRole.USER, blocks=[ImageBlock(path=Path("output.png")), TextBlock(text=f"Could you (1) evaluate the faithfulness of the attached image to this prompt: '{prompt}', (2) evaluate the quality of the image and (3) produce a description of the image that is agnostic of the prompt that was used to generate it?")])]
    resp = await llm_struct.achat(messages=messages)
    struct_output = json.loads(resp.message.blocks[0].text)
    return f"The generated image can be described as:\n'''\n{struct_output['prompt_agnostic_description']}\n'''\nThe faithfulness of the generated image to the original prompt is: {struct_output['faithfulness']}%.\nThe quality of the image is {struct_output['quality']}."
