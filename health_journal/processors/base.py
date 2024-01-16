from abc import ABC, abstractmethod

from health_journal.constants import PROCESSORS
from health_journal.notion.data import NoitonPage, NoitonTable
from health_journal.settings_secret import AUTH_KEY


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


class NotionTableProcessor(Processor):
    """
    Processor which connects to notion table using name of table
    """
    @property
    @abstractmethod
    def name(self):
        pass

    def __init__(self, auth_key=AUTH_KEY):
        self.database = NoitonTable(self.name, auth_key)


class NotionPageProcessor(Processor):
    """
    Processor which connects to notion page using name of page
    """
    @property
    @abstractmethod
    def name(self):
        pass

    def __init__(self, auth_key=AUTH_KEY):
        self.database = NoitonPage(self.name, auth_key)


def register_processor(cls):
    """
    Decorator for registering processor for using in main.py

    TODO: move to yaml config outside of code
    """
    PROCESSORS.append(cls())
    return cls
