import os
import requests
from dotenv import load_dotenv
from typing import Optional

# Load environment variables
load_dotenv()

# Configuration
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1/chat/completions"
DEFAULT_MODEL = "openai/gpt-3.5-turbo"
DEFAULT_MAX_TOKENS = 200
SYSTEM_PROMPT = "You are a helpful assistant."

def get_chatbot_response(user_input: str,
                         model: str = DEFAULT_MODEL,
                         max_tokens: int = DEFAULT_MAX_TOKENS,
                         system_prompt: str = SYSTEM_PROMPT) -> Optional[str]:
    """
    Send a message to the OpenRouter Chat API and return the model's response.

    Args:
        user_input (str): The message from the user.
        model (str): The model to use via OpenRouter.
        max_tokens (int): The maximum number of tokens in the response.
        system_prompt (str): Instruction for the AI's behavior.

    Returns:
        str | None: The AI's reply text, or None if the request fails.
    """
    if not OPENROUTER_API_KEY:
        return "OpenRouter API key not found. Please check your environment variables."
    
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input}
        ],
        "max_tokens": max_tokens
    }
    
    try:
        response = requests.post(OPENROUTER_BASE_URL, headers=headers, json=data)
        
        if response.status_code == 200:
            response_data = response.json()
            return response_data["choices"][0]["message"]["content"].strip()
        elif response.status_code == 401:
            return "Authentication failed. Please check your OpenRouter API key."
        elif response.status_code == 429:
            return "Rate limit exceeded. Please try again later."
        elif response.status_code == 400:
            return f"Bad request: {response.json().get('error', {}).get('message', 'Invalid request')}"
        else:
            return f"API request failed with status {response.status_code}: {response.text}"
            
    except requests.exceptions.ConnectionError:
        return "Network error. Please check your internet connection."
    except requests.exceptions.Timeout:
        return "Request timed out. Please try again."
    except requests.exceptions.RequestException as e:
        return f"Request error: {e}"
    except KeyError as e:
        return f"Unexpected response format: {e}"
    except Exception as e:
        return f"An unknown error occurred: {e}"