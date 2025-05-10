import os
from dotenv import load_dotenv

# Only load .env in non-production environments
if os.getenv("ENV") != "production":
    load_dotenv()