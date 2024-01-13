import json
from abc import ABC, abstractmethod
from pathlib import Path

import notion_client
import pandas as pd

from health_journal.constants import NOTION_DATABASE_IDS, NOTION_PAGES_IDS, PROCESSORS
from health_journal.settings_secret import AUTH_KEY
from health_journal.utils import save_page


class Processor(ABC):
    """
    Base Processor users requests
    """

    @abstractmethod
    def process(self, request):
        """
        Process request and return response

        Args:
            request: str

        Returns:
            str: message for user
        """
        pass

    @abstractmethod
    def should_processed(self, request):
        """
        Determine this request should be processed by this processor

        Args:
            request: str

        Returns:
            bool
        """
        pass


class NotionProcessor(Processor):
    def __init__(self, auth_key=AUTH_KEY):
        self.notion = notion_client.Client(auth=auth_key)


class BackUpable(ABC):
    """
    Class responsible for backing up data
    """

    @abstractmethod
    def create_backup(self):
        """
        Backup data

        Returns:
            str: path to backup file
        """
        pass


class NotionTableProcessor(NotionProcessor, BackUpable):
    """
    Processor responsible for working with notion table

    Allow convert Notion to Pandas DataFrame
    """

    @property
    def NOTION_DATABASE_ID(self):
        return NOTION_DATABASE_IDS[self.name]

    @property
    @abstractmethod
    def name(self):
        pass

    def _extract_data(self, page_properties):
        entry_data = {}
        for key, value in page_properties.items():
            property_type = value.get("type")
            if property_type == "title":
                entry_data[key] = value["title"][0]["text"]["content"] if value["title"] else ""
            elif property_type == "rich_text":
                entry_data[key] = value["rich_text"][0]["text"]["content"] if value["rich_text"] else ""
            elif property_type in ["number", "date", "select"]:
                entry_data[key] = value[property_type].get("start") if property_type == "date" else value[property_type]
        return entry_data

    def to_pandas(self):
        pages = self.notion.databases.query(database_id=self.NOTION_DATABASE_ID)
        backup_data = [self._extract_data(page["properties"]) for page in pages.get("results", [])]
        return pd.DataFrame(backup_data)

    def create_backup(self):
        data = self.to_pandas()
        path = f"{self.name}.csv"
        data.to_csv(path, index=False)
        return path


class NotionPageProcessor(NotionProcessor, BackUpable):
    """
    Processor responsible for working with notion page

    Allow convert Notion Page to Pandas DataFrame
    """

    @property
    def NOTION_PAGE_ID(self):
        return NOTION_PAGES_IDS[self.name]

    @property
    @abstractmethod
    def name(self):
        pass

    def create_backup(self):
        folder = Path("backup") / f"{self.name}"
        save_page(self.notion, self.NOTION_PAGE_ID, folder)

        return folder

class Drawble(ABC):
    """
    Class responsible for drawing html plots
    """

    @abstractmethod
    def get_html(self):
        """
        Returns:
            str: html plot
        """
        pass


def register_processor(cls):
    """
    Decorator for registering processor for using in main.py

    TODO: move to yaml config outside of code
    """
    PROCESSORS.append(cls())
    return cls
