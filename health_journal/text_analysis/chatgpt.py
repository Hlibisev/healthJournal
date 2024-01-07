from functools import partial
from multiprocessing.pool import ThreadPool

import openai

from health_journal.settings_secret import OPENAI_KEY, OPENAI_ORG

openai.organization = OPENAI_ORG
openai.api_key = OPENAI_KEY


def request_gpt(text_request, model="gpt-3.5-turbo"):
    response = openai.ChatCompletion.create(model=model, messages=[{"role": "user", "content": text_request}])
    response = response.choices[0]["message"]["content"]

    return response


def parallel_request_gpt(text_requests, model="gpt-3.5-turbo"):
    request_gpt_with_model = partial(request_gpt, model=model)

    with ThreadPool(len(text_requests)) as p:
        responses = p.map(request_gpt_with_model, text_requests)

    return responses
