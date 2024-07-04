import os
from dotenv import load_dotenv

# Load environment variables from .env file

load_dotenv()

# Get the API key from the environment variable
SECRET_KEY = os.getenv("secret_key")