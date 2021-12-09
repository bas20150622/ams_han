########
# Check existence of HOME_ID in .env file
# Check that home id can be found under the tibber token subscription
########

from config import TIBBER_TOKEN
import os
from queries import do_query, home_query


def test_exists():
    """Check that home_id is present in .env file"""
    assert os.getenv("HOME_ID"), "Error: HOME_ID not found in .env file "


def test_homeid():
    """Check that the provideded .env HOME_ID is valid for this subscription"""
    data = do_query(home_query)

    assert not data.get("errors", False), "Error: issue with provided TIBBER_TOKEN"
    home_ids = (home["id"] for home in data["data"]["viewer"]["homes"])
    assert (
        os.getenv("HOME_ID") in home_ids
    ), "Error: provided home id not found in subscription"
