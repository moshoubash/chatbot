import os
from dotenv import load_dotenv
from typing import Optional
from openai import OpenAI, OpenAIError, RateLimitError, APIConnectionError, BadRequestError, AuthenticationError

# Load environment variables
load_dotenv()

# Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
DEFAULT_MODEL = "gpt-4o-mini"
DEFAULT_MAX_TOKENS = 100
SYSTEM_PROMPT = "You are a helpful assistant."

# Initialize OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

def get_chatbot_response(user_input: str,
                         model: str = DEFAULT_MODEL,
                         max_tokens: int = DEFAULT_MAX_TOKENS,
                         system_prompt: str = SYSTEM_PROMPT) -> Optional[str]:
    """
    Send a message to the OpenAI Chat API and return the model's response.

    Args:
        user_input (str): The message from the user.
        model (str): The OpenAI model to use.
        max_tokens (int): The maximum number of tokens in the response.
        system_prompt (str): Instruction for the AI's behavior.

    Returns:
        str | None: The AI's reply text, or None if the request fails.
    """
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input}
            ],
            max_tokens=max_tokens
        )
        return response.choices[0].message.content.strip()
    except AuthenticationError:
        return "Authentication failed. Please check your API key."
    except RateLimitError:
        return "Rate limit exceeded. Please try again later."
    except APIConnectionError:
        return "Network error. Please check your connection."
    except BadRequestError as e:
        return f"Invalid request: {e}"
    except OpenAIError as e:
        return f"An unexpected API error occurred: {e}"
    except Exception as e:
        return f"An unknown error occurred: {e}"
