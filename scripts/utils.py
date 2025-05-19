from os import environ as ENV
from dotenv import load_dotenv
from typing import Tuple

def get_api_keys() -> Tuple[str, str]:
    openai_api_key = ENV.get("OPENAI_API_KEY", None)
    if openai_api_key is None:
        load_dotenv()
        openai_api_key = ENV.get("OPENAI_API_KEY", None)
        if not openai_api_key:
            raise ValueError("There is no OPENAI_API_KEY declared among the environmental variables")
    google_api_key = ENV.get("GOOGLE_API_KEY", None)
    if google_api_key is None:
        load_dotenv()
        google_api_key = ENV.get("GOOGLE_API_KEY", None)
        if not google_api_key:
            raise ValueError("There is no GOOGLE_API_KEY declared among the environmental variables")
    return openai_api_key, google_api_key
