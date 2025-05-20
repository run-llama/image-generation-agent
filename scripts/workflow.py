from tools import generate_image, evaluate_generated_image
from llama_index.core.agent.workflow import AgentWorkflow, FunctionAgent

image_generation_agent = FunctionAgent(
    name = "ImageGenerationAgent",
    description= "An Agent suitable for internal feedback-driven generation of  images",
    tools = [generate_image, evaluate_generated_image],
    system_prompt = "You are the ImageGenerationAgent. Your task is to generate images, evaluate them and, based on the feedback from the evaluation, re-generate them or return them to the user. Specifically, you need to follow these steps:\n" \
    "1. Generate an image starting from the user's prompt with the 'generate_image' tool.\n" \
    "2. Evaluate the generated image using the 'evaluate_generated_image' tool\n" \
    "If you deem the evaluation positive:\n" \
    "3. Return the image to the user, telling them what you generated\n" \
    "Else:\n" \
    "3. Refine the prompt for image generation, and go back to step 1\n" \
    "Do not stop unless you generated an image that suits the original prompt from the user.\n",
)

workflow = AgentWorkflow(
    agents = [image_generation_agent],
    root_agent= image_generation_agent.name,
    timeout=600,
)
