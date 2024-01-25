from datetime import datetime

from health_journal.processors.base import NotionTableProcessor, register_processor
from health_journal.text_analysis.chatgpt import parallel_request_gpt
from health_journal.text_analysis.prompts import emo_summary_prompt, format_prompt


@register_processor
class EmotionsDiaryProcessor(NotionTableProcessor):
    """
    Emotions diary processor

    Save emotions diary to Notion table

    Example:
        >>> emotions = EmotionsDiaryProcessor()
        >>> emotions.process("Сейчас состояние в целом нормальное, но есть небольшая тревога и усталость ...")
        >>> emotions.process("Добавь в дневник. Очень сонный.")
    """

    name = "emotions"

    def should_processed(self, request):
        return "дневник" in request

    def process(self, request):
        summary, text = self._format_text(request)
        self._write(summary, text)
        return "Добавлено в дневник самочувствия 🙂"

    def _write(self, summary, text):
        current_date = datetime.now().isoformat()

        self.database.add_data([
            ("Summary", "title", summary),
            ("Описание", "rich_text", text),
            ("Date", "date", current_date),
        ])

    def _format_text(self, request):
        summary_request = emo_summary_prompt(request)
        format_text_request = format_prompt(request)
        summary, text = parallel_request_gpt([summary_request, format_text_request])
        return summary, text
