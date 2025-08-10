import os
import requests
from dataclasses import dataclass
from dotenv import load_dotenv
from typing import Optional

# Load environment variables
load_dotenv()


@dataclass(frozen=True)
class ChatConfig:
    api_key: str = os.getenv("OPENROUTER_API_KEY", "")
    base_url: str = "https://openrouter.ai/api/v1/chat/completions"
    default_model: str = "openai/gpt-3.5-turbo"
    default_max_tokens: int = 300
    default_system_prompt: str = "You are a helpful assistant."
    request_timeout: int = 15  # seconds

CONFIG = ChatConfig()

def _build_headers() -> dict:
    """Prepare request headers."""
    return {
        "Authorization": f"Bearer {CONFIG.api_key}",
        "Content-Type": "application/json"
    }

def _build_payload(user_input: str, model: str, max_tokens: int, system_prompt: str) -> dict:
    """Prepare API request payload."""
    return {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input}
        ],
        "max_tokens": max_tokens
    }

def get_chatbot_response(
    user_input: str,
    model: str = CONFIG.default_model,
    max_tokens: int = CONFIG.default_max_tokens,
    system_prompt: str = CONFIG.default_system_prompt
) -> Optional[str]:
    """
    Send a message to the OpenRouter Chat API and return the model's response.
    """
    if not CONFIG.api_key:
        return "OpenRouter API key not found. Please check your environment variables."

    try:
        response = requests.post(
            CONFIG.base_url,
            headers=_build_headers(),
            json=_build_payload(user_input, model, max_tokens, system_prompt),
            timeout=CONFIG.request_timeout
        )

        # Handle non-success HTTP codes
        if response.status_code != 200:
            return _handle_error(response)

        # Parse and return response text
        return response.json()["choices"][0]["message"]["content"].strip()

    except requests.exceptions.Timeout:
        return "Request timed out. Please try again."
    except requests.exceptions.ConnectionError:
        return "Network error. Please check your internet connection."
    except requests.exceptions.RequestException as e:
        return f"Request error: {e}"
    except (KeyError, IndexError) as e:
        return f"Unexpected response format: {e}"
    except Exception as e:
        return f"An unknown error occurred: {e}"


def _handle_error(response: requests.Response) -> str:
    """Map HTTP errors to friendly messages."""
    status_map = {
        400: f"Bad request: {response.json().get('error', {}).get('message', 'Invalid request')}",
        401: "Authentication failed. Please check your OpenRouter API key.",
        429: "Rate limit exceeded. Please try again later."
    }
    return status_map.get(response.status_code, f"API request failed: {response.status_code} {response.text}")
