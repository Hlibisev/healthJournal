import os

from dotenv import load_dotenv

load_dotenv()


AUTH_KEY = os.getenv("AUTH_KEY")
OPENAI_ORG = os.getenv("OPENAI_ORG")
OPENAI_KEY = os.getenv("OPENAI_KEY")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
BUCKET_NAME = os.getenv("BUCKET_NAME")
