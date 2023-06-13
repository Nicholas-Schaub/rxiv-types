import time
from pathlib import Path

import pytest
import requests

from rxiv_types import arxiv_records

chemrxiv_url = (
    "https://export.arxiv.org/oai2?verb=ListRecords&metadataPrefix=oai_dc&from={}"
)


@pytest.fixture(
    params=[
        "2020-07-01T00:00:00Z",
        "2021-01-01T00:00:00Z",
        "2021-07-01T00:00:00Z",
        "2022-01-01T00:00:00Z",
        "2022-07-01T00:00:00Z",
    ]
)
def arxiv_set(request) -> Path:
    # Need a delay since they have a 1 request/5 seconds rate limit
    time.sleep(5)

    page = request.param
    result = requests.get(chemrxiv_url.format(page))
    destination = Path(f"downloads/data/arxiv{page}.xml")
    destination.parent.mkdir(parents=True, exist_ok=True)
    with open(destination, "wb") as fw:
        fw.write(result.content)

    return destination


def test_arxiv(arxiv_set):
    result = arxiv_records(arxiv_set)
