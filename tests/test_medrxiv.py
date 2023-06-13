from pathlib import Path

import pytest
import requests

from rxiv_types import medrxiv_records

medrxiv_url = "https://api.medrxiv.org/details/medrxiv/2000-01-01/2020-01-01/{}/xml"


@pytest.fixture(params=list(range(1, 1000, 200)))
def medrxiv_set(request) -> Path:
    page = request.param
    result = requests.get(medrxiv_url.format(page))
    destination = Path(f"downloads/data/medrxiv{page}.xml")
    destination.parent.mkdir(parents=True, exist_ok=True)
    with open(destination, "wb") as fw:
        fw.write(result.content)

    return destination


def test_medarxiv(medrxiv_set):
    result = medrxiv_records(medrxiv_set)
