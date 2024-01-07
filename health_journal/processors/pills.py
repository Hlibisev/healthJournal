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
        name, dose, status = self.get_pill_info(request)
        self.send_to_notion(name, dose, status)
        return f"💊 {name} {dose} " + ("🟢" if status == "начал" else "🔴")

    def send_to_notion(self, name, dose, status):
        current_date = datetime.now().isoformat()
        properties = {
            "Лекарство": {"title": [{"text": {"content": name}}]},
            "доза": {"rich_text": [{"text": {"content": dose}}]},
            "статус": {"select": {"name": status}},
            "Date": {"date": {"start": current_date}},
        }
        self.notion.pages.create(parent={"database_id": self.NOTION_DATABASE_ID}, properties=properties)

    @retry(stop=stop_after_attempt(3), retry=retry_if_exception_type(ValueError))
    def get_pill_info(self, request):
        request_body = medication_info_prompt(request)
        response = request_gpt(request_body)

        try:
            name, dose, status = response.split(",")
        except ValueError:
            message = f"Can't parse response: {response}"

            logging.warning(message + " Retrying...")
            raise ValueError(message)

        return name, dose, "начал" if "нач" in status else "закончил"
