from health_journal.constants import DATABASES, NOTION_DATABASE_IDS, NOTION_PAGES_IDS
from health_journal.logger import logger
from health_journal.notion.data import NoitonPage, NoitonTable
import health_journal.processors

DATABASES += [NoitonTable(name) for name in NOTION_DATABASE_IDS.keys()]
DATABASES += [NoitonPage(name) for name in NOTION_PAGES_IDS.keys()]


# TODO: hot fix health_journal.processors import