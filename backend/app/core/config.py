import os
from dotenv import load_dotenv
import openai

# Load environment variables from .env file
load_dotenv()

# OpenAI configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    print("Warning: OPENAI_API_KEY environment variable not set")

# Create OpenAI client
openai_client = openai.OpenAI(api_key=OPENAI_API_KEY)
