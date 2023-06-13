from pathlib import Path

import pytest
import requests

from rxiv_types import biorxiv_records

biorxiv_url = "https://api.biorxiv.org/details/biorxiv/2000-01-01/2020-01-01/{}/xml"
medrxiv_url = "https://api.medrxiv.org/details/medrxiv/2000-01-01/2020-01-01/{}/xml"


@pytest.fixture(params=list(range(1, 90000, 20000)))
def biorxiv_set(request) -> Path:
    page = request.param
    result = requests.get(biorxiv_url.format(page))
    destination = Path(f"downloads/data/biorxiv{page}.xml")
    destination.parent.mkdir(parents=True, exist_ok=True)
    with open(destination, "wb") as fw:
        fw.write(result.content)

    return destination


def test_bioarxiv(biorxiv_set):
    result = biorxiv_records(biorxiv_set)
