import asyncio
import signal
import time
from functools import partial
import logging
from python_graphql_client import GraphqlClient
import os
from config import TIBBER_TOKEN
from subscriptions import subscribe, livemeasurent_detailed_subscription
from data_handlers import ValidSubscriptionData
from typing import Callable


class MyException(Exception):
    pass


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

    handler = ValidSubscriptionData()

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
            subscribe(
                subscription_query=livemeasurent_detailed_subscription,
                subscription_handler=handler.print,
            )
        )
        loop.run_forever()
    finally:
        loop.close()
        logging.info("Successfully shutdown the live measurements service.")


if __name__ == "__main__":
    main()
