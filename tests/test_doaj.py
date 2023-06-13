from pathlib import Path

import pytest
import requests

from rxiv_types import doaj_records

doaj_url = (
    "https://www.doaj.org/oai.article?verb=ListRecords&metadataPrefix=oai_dc&from={}"
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
def doaj_set(request) -> Path:
    page = request.param
    result = requests.get(doaj_url.format(page))
    destination = Path(f"downloads/data/doaj{page}.xml")
    destination.parent.mkdir(parents=True, exist_ok=True)
    with open(destination, "wb") as fw:
        fw.write(result.content)

    return destination


def test_doaj(doaj_set):
    result = doaj_records(doaj_set)
