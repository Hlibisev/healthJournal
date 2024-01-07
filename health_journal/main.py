import logging

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

from health_journal.constants import PROCESSORS
from health_journal.processors.base import Drawble

app = FastAPI()


class Request(BaseModel):
    command: str


@app.post("/process/")
async def process_request(request: Request):
    """
    Process request and return beaty response
    """

    logging.info(f"Starting command... \n {request.command}")

    request = request.command.lower()
    res = "Запрос не обработан ❌"

    for processor in PROCESSORS:
        if processor.should_processed(request):
            res = processor.process(request)
            break

    return {"response": res}


@app.get("/{plot_name}_plot/", response_class=HTMLResponse)
async def process_plot(plot_name: str):
    """
    Return corresponding html plot
    """
    for processor in PROCESSORS:
        if str(processor) == plot_name and isinstance(processor, Drawble):
            html = processor.get_html()
            return html

    logging.error(f"Plot {plot_name} not found")


# @app.on_event("startup")
# async def startup_event():
#     """
#     Set up everyday backup
#     """
#     backuper = BackUper()
#     backuper.backup_everyday(PROCESSORS)
