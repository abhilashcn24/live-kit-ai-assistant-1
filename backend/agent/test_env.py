import os
from dotenv import load_dotenv

load_dotenv()

print("GMAIL_PASSWORD:", os.getenv("GMAIL_PASSWORD"))
