import urllib.request as request
from contextlib import closing
from pathlib import Path

import nox


@nox.session
def generate_packages(session):
    session.install("requests", "xsdata-pydantic[cli,lxml,soap]")

    # Get the article schema
    base_path = Path("downloads/schemas")
    base_path.mkdir(exist_ok=True, parents=True)

    rxivs = {
        "oai_pmh": ("oai_pmh", "http://www.openarchives.org/OAI/2.0/OAI-PMH.xsd"),
        "biorxiv": ("biorxiv", "https://api.biorxiv.org/oaipmh/bioRxivRaw/"),
        "medrxiv": ("medrxiv", "https://api.biorxiv.org/OAI/medRxivRaw.xsd"),
        # "dc": (
        #     "oai_dc",
        #     "https://www.dublincore.org/schemas/xmls/simpledc20021212.xsd",
        # ),
        # "dcterms": (
        #     "dcterms",
        #     "https://www.dublincore.org/schemas/xmls/qdc/2008/02/11/dcterms.xsd",
        # ),
        "oai_dc": ("oai_dc", "http://www.openarchives.org/OAI/2.0/oai_dc/"),
    }

    for rxiv_name, (namespace, rxiv_url) in rxivs.items():
        with closing(request.urlopen(rxiv_url)) as url:
            with open(base_path.joinpath(rxiv_name + ".xsd"), "wb") as fw:
                fw.write(url.read())

        # Generate the models
        session.run(
            "xsdata",
            f"downloads/schemas/{rxiv_name + '.xsd'}",
            "--output",
            "pydantic",
            "--package",
            f"src.rxiv_types.models.{namespace}",
            "--structure-style",
            "namespace-clusters",
            "--relative-imports",
            "--debug",
        )

    # Adjust for bug in medrxiv API results
    medrxiv_files = [
        "src/rxiv_types/models/medrxiv/https/api/bio_rxiv/org/oaipmh/med_rxiv_raw/med_rxiv_raw.py",
        "src/rxiv_types/models/medrxiv/https/api/bio_rxiv/org/oaipmh/med_rxiv_raw/med_rxiv_raw_type.py",
    ]
    bug_ns = "https://api.bioriv.org/OAI/medRxivRaw/"
    correct_ns = "https://api.bioRxiv.org/oaipmh/medRxivRaw/"
    for file in medrxiv_files:
        with open(file, "r") as fr:
            code = fr.read()

        with open(file, "w") as fw:
            fw.write(code.replace(correct_ns, bug_ns))

    # Remove extraneous __init__ file
    Path("src/__init__.py").unlink()
