import asyncio
import signal
import time
from functools import partial
import logging
from python_graphql_client import GraphqlClient
import os
from config import TIBBER_TOKEN


class MyException(Exception):
    pass


def print_handle(data):
    print(
        data["data"]["liveMeasurement"]["timestamp"]
        + " "
        + str(data["data"]["liveMeasurement"]["power"])
    )


def handle_exception(loop, context):
    msg = context.get("exception", context["message"])
    logging.error(f"Caught exception: {msg}")
    logging.info("Shutting down...")
    time.sleep(1)
    asyncio.create_task(shutdown(loop))


async def shutdown(loop, signal=None):
    """
    Shutdown handler
    :param loop:
    :param db:
    :param executor:
    """
    if signal:
        logging.info(f"Received exit signal {signal.name}...")

    logging.info("Nacking outstanding tasks")
    tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]

    [task.cancel() for task in tasks]

    logging.info("Cancelling outstanding tasks")
    await asyncio.gather(*tasks, return_exceptions=True)

    loop.stop()


def main():
    logging.basicConfig(level=logging.INFO)

    client = GraphqlClient(endpoint="wss://api.tibber.com/v1-beta/gql/subscriptions")
    query = """
    subscription ($homeid: ID!){
    liveMeasurement(homeId:$homeid){
        timestamp
        power
    }
    }
    """

    variables = {"homeid": os.getenv("HOME_ID")}

    loop = asyncio.get_event_loop()
    loop.set_debug(True)

    signals = (signal.SIGHUP, signal.SIGTERM, signal.SIGINT)
    for s in signals:
        loop.add_signal_handler(
            s, lambda s=s: asyncio.create_task(shutdown(loop, signal=s))
        )
    loop.set_exception_handler(partial(handle_exception))

    try:
        loop.create_task(
            client.subscribe(
                query=query,
                variables=variables,
                headers={"Authorization": TIBBER_TOKEN},
                handle=print_handle,
            )
        )
        loop.run_forever()
    finally:
        loop.close()
        logging.info("Successfully shutdown the orderServer service.")


if __name__ == "__main__":
    main()
