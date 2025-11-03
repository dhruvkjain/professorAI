import os
from dotenv import load_dotenv

load_dotenv()

NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USER = os.getenv("NEO4J_USERNAME")
NEO4J_PASS = os.getenv("NEO4J_PASSWORD")
DEEP_INFRA_API_KEY = os.getenv("DEEP_INFRA_API_KEY")
DEEP_INFRA_API_URL = os.getenv("DEEP_INFRA_API_URL")
OPEN_AI_API_KEY = os.getenv("OPEN_AI_API_KEY")