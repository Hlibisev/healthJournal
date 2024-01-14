import logging
from datetime import datetime

from tenacity import retry, retry_if_exception_type, stop_after_attempt

from health_journal.processors.base import NotionTableProcessor, register_processor
from health_journal.text_analysis.chatgpt import request_gpt
from health_journal.text_analysis.prompts import medication_info_prompt


@register_processor
class PillsProcessor(NotionTableProcessor):
    """
    Pills processor

    Save pills to Notion table

    Example:
        >>> pills = PillsProcessor()
        >>> pills.process("заканчиваю прием витамин д 5000")
        >>> pills.process("начал принимать мелотонин 1 мг")
        >>> pills.process("омега 3 1000 единиц закончил")
        >>> pills.process("прекращаю принимать экстракт зеленого чая")
    """

    name = "pills"

    def should_processed(self, request):
        return "принимать" in request and len(request) < 100

    def process(self, request):
        name, dose, status = self._extract_info(request)
        self._write(name, dose, status)
        return f"💊 {name} {dose} " + ("🟢" if status == "начал" else "🔴")

    def _write(self, name, dose, status):
        current_date = datetime.now().isoformat()

        self.database.add_data([
            ("Лекарство", "title", name),
            ("доза", "rich_text", dose),
            ("статус", "select", status),
            ("Date", "date", current_date),
        ])

    @retry(stop=stop_after_attempt(3), retry=retry_if_exception_type(ValueError))
    def _extract_info(self, request):
        request_body = medication_info_prompt(request)
        response = request_gpt(request_body)

        try:
            name, dose, status = response.split(",")
        except ValueError:
            message = f"Can't parse response: {response}"

            logging.warning(message + " Retrying...")
            raise ValueError(message)

        return name, dose, "начал" if "нач" in status else "закончил"
