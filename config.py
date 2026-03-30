import os
from dotenv import load_dotenv

load_dotenv()

CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY")
TARGET_URL = os.getenv("TARGET_URL", "https://automationexercise.com/")
OUTPUT_FILE = os.getenv("OUTPUT_FILE", "output/test_cases.xlsx")
MODEL = os.getenv("MODEL", "claude-3-sonnet-20240229")
