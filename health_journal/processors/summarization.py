from datetime import datetime, timedelta

import pandas as pd
import pytz

from health_journal.processors.base import NotionPageProcessor, register_processor
from health_journal.processors import EmotionsDiaryProcessor
from health_journal.utils import change_text_notion
from health_journal.text_analysis.chatgpt import request_gpt
from health_journal.text_analysis.prompts import SUMMARIZATION_HEALTH_PROMPT


@register_processor
class SummarizeProcessor(NotionPageProcessor):
    """
    Summarize processor

    Example:
        >>> summarizer = SummarizeProcessor()
        >>> summarizer.process()
        >>> summarizer.process(request)
    """

    name = "summarize"

    def should_processed(self, request):
        return "сводк" in request

    def process(self, *_):
        text = self.get_summarization()
        change_text_notion(self.notion, self.NOTION_PAGE_ID, text)
        return "Суммаризация выполнена ✅"

    def get_summarization(self):
        emotioin_df = EmotionsDiaryProcessor().to_pandas()

        emotioin_df["Date"] = pd.to_datetime(emotioin_df["Date"])
        start_date = (datetime.now() - timedelta(days=60)).replace(tzinfo=pytz.UTC)
        emotioin_df = emotioin_df[emotioin_df["Date"] > start_date]

        emotioin_df["Date"] = emotioin_df["Date"].apply(lambda x: x.strftime("%Y-%m-%d %H"))

        records = emotioin_df["Date"] + ", " + emotioin_df["Описание"]
        records = "\n".join(records)
        request = SUMMARIZATION_HEALTH_PROMPT + records

        summatization = "\n" + request_gpt(request)
        return summatization
