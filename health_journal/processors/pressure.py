from datetime import datetime

from health_journal.processors.base import NotionTableProcessor, register_processor


@register_processor
class BloodPressureProcessor(NotionTableProcessor):
    """
    Blood pressure processor

    Save blood pressure to Notion table

    Example:
        >>> bloodpressure = BloodPressureProcessor()
        >>> bloodpressure.process("давление 120 80")
        >>> bloodpressure.process("давление было 130 на 90")
        >>> bloodpressure.process("давление: 115 к 75")
    """

    name = "pressure"

    def should_processed(self, request):
        return "давление" in request

    def process(self, request):
        upper, lower = self._extract_info(request)
        self._write(upper, lower, text=request)
        return f"🫀 Давление {upper}" + (f" на {lower}" if lower else "")

    def _write(self, upper, lower=None, text=""):
        current_date = datetime.now().isoformat()

        data = [
            ("Date", "date", current_date),
            ("Upper", "number", int(upper)),
            ("Full text", "title", text),
        ]

        if lower:
            data.append(("Lower", "number", int(lower)))

        self.database.add_data(data)


    def _extract_info(self, request):
        """
        Extract upper and lower values from request
        """
        pressure_values = [word for word in request.split() if word.isdigit()]
        return pressure_values[:2] if len(pressure_values) >= 2 else (pressure_values[0], None)
