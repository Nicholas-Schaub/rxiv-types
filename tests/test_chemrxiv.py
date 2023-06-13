from pathlib import Path

import pytest
import requests

from rxiv_types import chemrxiv_records

chemrxiv_url = "https://chemrxiv.org/engage/chemrxiv/public-api/v1/oai?verb=ListRecords&metadataPrefix=oai_dc&from={}"


@pytest.fixture(
    params=[
        "2020-07-01T00:00:00Z",
        "2021-01-01T00:00:00Z",
        "2021-07-01T00:00:00Z",
        "2022-01-01T00:00:00Z",
        "2022-07-01T00:00:00Z",
    ]
)
def chemrxiv_set(request) -> Path:
    page = request.param
    result = requests.get(chemrxiv_url.format(page))
    destination = Path(f"downloads/data/chemrxiv{page}.xml")
    destination.parent.mkdir(parents=True, exist_ok=True)
    with open(destination, "wb") as fw:
        fw.write(result.content)

    return destination


def test_chemrxiv(chemrxiv_set):
    result = chemrxiv_records(chemrxiv_set)
