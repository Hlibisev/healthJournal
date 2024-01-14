import datetime
from abc import abstractmethod
from pathlib import Path

import notion_client
import pandas as pd

from health_journal.constants import NOTION_DATABASE_IDS, NOTION_PAGES_IDS
from health_journal.notion.cells import cells
from health_journal.settings_secret import AUTH_KEY
from health_journal.utils import save_page, text_block


class DataBase:
    @abstractmethod
    def create_backup(self):
        pass

    @abstractmethod
    def add_data(self, data):
        pass


class NotionData(DataBase):
    def __init__(self, auth_key=AUTH_KEY) -> None:
        self.notion = notion_client.Client(auth=auth_key)


class NoitonTable(NotionData):
    def __init__(self, name="", auth_key=AUTH_KEY) -> None:
        super().__init__(auth_key)

        assert name in NOTION_DATABASE_IDS.keys(), f"Database with name {name} not found"
        self.name = name

    @property
    def NOTION_DATABASE_ID(self):
        return NOTION_DATABASE_IDS[self.name]

    def add_data(self, data):
        """
        Add data to table

        Args:
            data (list): list "column_name", "type", "value"
        """
        properties = {}

        for column_name, column_type, value in data:
            properties[column_name] = cells[column_type](value)

        new_entry = {"parent": {"database_id": self.NOTION_DATABASE_ID}, "properties": properties}
        self.notion.pages.create(**new_entry)

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


class NoitonPage(NotionData):
    def __init__(self, name="", auth_key=AUTH_KEY) -> None:
        super().__init__(auth_key)

        assert name in NOTION_PAGES_IDS.keys(), f"Page with name {name} not found"
        self.name = name

    @property
    def NOTION_PAGE_ID(self):
        return NOTION_PAGES_IDS[self.name]

    def add_data(self, text):
        """
        Change text in first block of notion page

        Args:
            text (str): New text
        """

        current_blocks = self.notion.blocks.children.list(block_id=self.NOTION_PAGE_ID)["results"]

        first_id = current_blocks[0]["id"]
        self.notion.blocks.update(block_id=first_id, **text_block(text))

    def create_backup(self):
        folder = Path("backup") / f"{self.name}"
        save_page(self.notion, self.NOTION_PAGE_ID, folder)

        return folder
