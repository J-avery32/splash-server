import pytest
import json
from .testing_utils import generic_test_api_crud


@pytest.mark.usefixtures("splash_client", "token_header")
def test_flask_crud_user(api_url_root, splash_client, token_header):
    generic_test_api_crud(
        new_page, api_url_root + "/pages", splash_client, token_header
    )


def test_no_empty_strings(api_url_root, splash_client, token_header):
    url = api_url_root + "/pages"
    response = splash_client.post(
        url, data=json.dumps(empty_string_metadata_title), headers=token_header
    )
    assert (
        response.status_code == 422
    ), f"{response.status_code}: response is {response.content}"
    response = splash_client.post(
        url, data=json.dumps(empty_string_metadata_text), headers=token_header
    )
    assert (
        response.status_code == 422
    ), f"{response.status_code}: response is {response.content}"
    response = splash_client.post(
        url, data=json.dumps(empty_string_section_title), headers=token_header
    )
    assert (
        response.status_code == 422
    ), f"{response.status_code}: response is {response.content}"
    response = splash_client.post(
        url, data=json.dumps(empty_string_section_text), headers=token_header
    )
    assert (
        response.status_code == 422
    ), f"{response.status_code}: response is {response.content}"
    response = splash_client.post(
        url, data=json.dumps(empty_string_title), headers=token_header
    )
    assert (
        response.status_code == 422
    ), f"{response.status_code}: response is {response.content}"


def test_retrieve_by_type(api_url_root, splash_client, token_header):
    url = api_url_root + "/pages"
    response = splash_client.post(
        url,
        data=json.dumps(
            {
                "title": "Drake",
                "page_type": "mythical_animals",
                "metadata": [],
                "documentation": [],
            }
        ),
        headers=token_header,
    )
    assert (
        response.status_code == 200
    ), f"{response.status_code}: response is {response.content}"
    response = splash_client.post(
        url,
        data=json.dumps(
            {
                "title": "Troll",
                "page_type": "mythical_animals",
                "metadata": [],
                "documentation": [],
            }
        ),
        headers=token_header,
    )
    assert (
        response.status_code == 200
    ), f"{response.status_code}: response is {response.content}"
    response = splash_client.post(
        url,
        data=json.dumps(
            {
                "title": "Wand",
                "page_type": "mythical_items",
                "metadata": [],
                "documentation": [],
            }
        ),
        headers=token_header,
    )
    assert (
        response.status_code == 200
    ), f"{response.status_code}: response is {response.content}"

    response = splash_client.get(
        url + "/page_type/mythical_animals", headers=token_header
    )
    assert (
        response.status_code == 200
    ), f"{response.status_code}: response is {response.content}"
    resp_obj = response.json()
    assert len(resp_obj) == 2
    assert any(page["title"] == "Drake" for page in resp_obj)
    assert any(page["title"] == "Troll" for page in resp_obj)


new_page = {
    "title": "Boron",
    "page_type": "compound",
    "metadata": [{"title": "contributors", "text": "Matt Landsman, Lauren Nalley"}],
    "documentation": {
        "sections": [
            {
                "title": "Relevance to M-WET:",
                "text": "- Naturally occurring in the environment\n\t - Seawater concentration around 5 mg/L [[1]](#1)\
                \n - Toxicity\n\t - boron has an extremely narrow concentration range between deficiency and toxicity \
                in some plants [[2]](#2) and it has been shown to suppress plant growth [[3]](#3) and immune response \
                in several crops [[4]](#4) .\n - Small, neutral solute\n\t - Boric acid is a small solute, with an \
                estimated Stokes radius of 1.6 Å [[5]](#5) , compared to 1.8 Å and 1.2 Å for sodium and chloride, \
                respectively [[6]](#6) .\n\t - The Stokes radius of borate has been estimated as 2.6 Å [[7]](#7) .",
            },
        ]
    },
}

empty_string_title = {
    "title": "",
    "page_type": "compound",
    "metadata": [{"title": "contributors", "text": "Matt Landsman, Lauren Nalley"}],
    "documentation": {
        "sections": [
            {
                "title": "Internal publications",
                "text": " - Landsman, Lawler, Katz (2020). Application of electrodialysis pretreatment to enhance boron \
                    removal and reduce fouling during nanofiltration/reverse osmosis",
            }
        ]
    },
}

empty_string_metadata_title = {
    "title": "Boron",
    "page_type": "compound",
    "metadata": [{"title": "", "text": "Matt Landsman, Lauren Nalley"}],
    "documentation": {
        "sections": [
            {
                "title": "Internal publications",
                "text": " - Landsman, Lawler, Katz (2020). Application of electrodialysis pretreatment to enhance boron \
                removal and reduce fouling during nanofiltration/reverse osmosis",
            }
        ]
    },
}

empty_string_metadata_text = {
    "title": "",
    "page_type": "compound",
    "metadata": [{"title": "contributors", "text": ""}],
    "documentation": {
        "sections": [
            {
                "title": "Internal publications",
                "text": " - Landsman, Lawler, Katz (2020). Application of electrodialysis pretreatment to enhance boron \
                    removal and reduce fouling during nanofiltration/reverse osmosis",
            }
        ]
    },
}

empty_string_section_title = {
    "title": "Boron",
    "page_type": "compound",
    "metadata": [{"title": "contributors", "text": "Matt Landsman, Lauren Nalley"}],
    "documentation": {
        "sections": [
            {
                "title": "",
                "text": " - Landsman, Lawler, Katz (2020). Application of electrodialysis pretreatment to enhance boron \
                    removal and reduce fouling during nanofiltration/reverse osmosis",
            }
        ]
    },
}

empty_string_section_text = {
    "title": "Boron",
    "page_type": "compound",
    "metadata": [{"title": "contributors", "text": "Matt Landsman, Lauren Nalley"}],
    "documentation": {"sections": [{"title": "Internal publications", "text": ""}]},
}
