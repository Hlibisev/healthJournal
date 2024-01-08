import os
from typing import List

from dotenv import load_dotenv

load_dotenv()

# Mapping of Notion database names to their IDs
NOTION_DATABASE_IDS = {
    "pressure": os.getenv("PRESSURE_NOTION_DATABASE_ID"),
    "pills": os.getenv("PILLS_NOTION_DATABASE_ID"),
    "emotions": os.getenv("EMOTION_NOTION_DATABASE_ID"),
}

NOTION_PAGES_IDS = {
    "summarize": os.getenv("SUMMARIZE_NOTION_PAGE_ID"),
}

# Processors autimatically registered using health_journal.processors.base.register_processor
PROCESSORS: "List[Processor]" = []  # noqa: F821
