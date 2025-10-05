
import os
from dotenv import load_dotenv

load_dotenv()  

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY")
# Optional: for image generation or LinkedIn publishing---not yet made
STABILITY_API_KEY = os.getenv("STABILITY_API_KEY")
LINKEDIN_CLIENT_ID = os.getenv("LINKEDIN_CLIENT_ID")
LINKEDIN_CLIENT_SECRET = os.getenv("LINKEDIN_CLIENT_SECRET")
