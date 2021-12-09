# Script to generate .env file containing key for Tibber API
# also attempts to add a home ID if found using the Tibber API key
from pathlib import Path
from dotenv import load_dotenv
import os


def main():
    ENV_FILE = Path(".env")
    if not ENV_FILE.exists():
        # create .env
        ENV_FILE.touch()

    # load .env
    load_dotenv()

    # check TIBBER_TOKEN env variable
    TIBBER_TOKEN = os.getenv("TIBBER_TOKEN")
    if not TIBBER_TOKEN:
        print("tibber API token not found...")
        while True:
            resp = input("add API token manually now? (yes/no): ")
            resp = resp.upper()
            if resp in ["N", "NO"]:
                return
            elif resp in ["YES", "Y"]:
                TIBBER_TOKEN = input("please enter tibber API token and press enter: ")
                # DO SOME CHECKING
                if not len(TIBBER_TOKEN) == 43:
                    print("Error: wrong token length")
                    continue
                ENV_FILE.write_text("TIBBER_TOKEN=" + TIBBER_TOKEN + "\n")
                break

    # check if a home id can be found
    HOME_ID = os.getenv("HOME_ID")
    if not HOME_ID:
        print("Home ID not found...")
        while True:
            resp = input("attempt to retrieve (first) Home ID? (yes/no): ")
            resp = resp.upper()
            if resp in ["N", "NO"]:
                break
            elif resp in ["YES", "Y"]:
                from queries import do_query, home_query

                home_data = do_query(home_query)
                if not home_data:
                    print("Error: can not retrieve home ids, is the token correct?")
                home_ids = [home["id"] for home in home_data["data"]["viewer"]["homes"]]
                if len(home_ids) > 1:
                    print(f"multiple home IDs found, adding first of {home_ids}")
                if home_ids:
                    with ENV_FILE.open("a") as f:
                        f.write("HOME_ID=" + home_ids[0] + "\n")
                break
    print("all done...")


main()
