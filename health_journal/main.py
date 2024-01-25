from fastapi import FastAPI
from pydantic import BaseModel

from health_journal.backuper import BackUper
from health_journal.constants import DATABASES, PROCESSORS
from health_journal import logger

app = FastAPI()


class Request(BaseModel):
    command: str


@app.post("/process/")
async def process_request(request: Request):
    """
    Process request and return beaty response
    """
    logger.info(f"Starting command... \n {request.command}")

    request = request.command.lower()
    res = "Запрос не обработан ❌"

    for processor in PROCESSORS:
        if processor.should_processed(request):
            res = processor.process(request)
            break

    return {"response": res}


@app.on_event("startup")
async def startup_event():
    """
    Set up everyday backup
    """
    backuper = BackUper(DATABASES)
    backuper.backup(hour=23)
