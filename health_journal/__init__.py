from health_journal.constants import DATABASES, NOTION_DATABASE_IDS, NOTION_PAGES_IDS
from health_journal.notion.data import NoitonPage, NoitonTable

DATABASES += [NoitonTable(name) for name in NOTION_DATABASE_IDS.keys()]
DATABASES += [NoitonPage(name) for name in NOTION_PAGES_IDS.keys()]
