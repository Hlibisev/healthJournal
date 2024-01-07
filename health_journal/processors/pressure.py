from datetime import datetime

import pandas as pd
import plotly.express as px
import plotly.io as pio

from health_journal.processors.base import Drawble, NotionTableProcessor, register_processor


@register_processor
class BloodPressureProcessor(NotionTableProcessor, Drawble):
    """
    Blood pressure processor

    Save blood pressure to Notion table

    Example:
        >>> bloodpressure = BloodPressureProcessor()
        >>> bloodpressure.process("давление 120 80")
        >>> bloodpressure.process("давление было 130 на 90")
        >>> bloodpressure.process("давление: 115 к 75")
        >>> html = bloodpressure.get_html()
    """

    name = "pressure"

    def should_processed(self, request):
        return "давление" in request

    def process(self, request):
        upper, lower = self.get_values(request)
        self.send_to_notion(upper, lower, text=request)
        return f"🫀 Давление {upper}" + (f" на {lower}" if lower else "")

    def send_to_notion(self, upper, lower=None, text=""):
        current_date = datetime.now().isoformat()
        new_entry = {
            "parent": {"database_id": self.NOTION_DATABASE_ID},
            "properties": {
                "Name": {"title": [{"text": {"content": ""}}]},
                "Date": {"date": {"start": current_date}},
                "Upper": {"number": int(upper)},
                "Full text": {"rich_text": [{"text": {"content": text}}]},
            },
        }
        if lower:
            new_entry["properties"]["Lower"] = {"number": int(lower)}
        self.notion.pages.create(**new_entry)

    def get_values(self, request):
        """
        Extract upper and lower values from request
        """
        pressure_values = [word for word in request.split() if word.isdigit()]
        return pressure_values[:2] if len(pressure_values) >= 2 else (pressure_values[0], None)

    def get_html(self):
        data = self.to_pandas()
        data["Date"] = pd.to_datetime(data["Date"])
        data = data.sort_values("Date")

        fig = px.line(
            data,
            x="Date",
            y="Upper",
            title="Blood Pressure Over Time",
            render_mode="svg",
        )

        fig.update_layout(
            template="plotly_white",
            xaxis_title="Date",
            yaxis_title="Blood Pressure (Upper)",
            font=dict(family="Arial, sans-serif", size=12, color="RebeccaPurple"),
            margin=dict(t=40, b=0, l=0, r=0),
        )
        fig.update_traces(line=dict(width=2.5))

        graph_html = pio.to_html(fig, full_html=False)

        return f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>My Plotly Graph</title>
            </head>
            <body>{graph_html}</body>
            </html>
        """
