# Library for subscriptions to tibber pulse API
from python_graphql_client import GraphqlClient
from typing import Callable, Dict
from config import TIBBER_TOKEN
import os

HOME_ID = os.getenv("HOME_ID")  # due to import of config, dotenv should be loaded

subscription_client = GraphqlClient(
    endpoint="wss://api.tibber.com/v1-beta/gql/subscriptions"
)


def livemeasurent_minimal_subscription() -> Dict[str, str]:
    """
    Query & variables to subscribe to timestamp and power
    :returns: dict {query: query_str, variables: query_variables}
    """
    query = """
    subscription ($homeid: ID!){
        liveMeasurement(homeId:$homeid){
            timestamp
            power
        }
    }
    """

    variables = {"homeid": os.getenv("HOME_ID")}

    return dict(zip(["query", "variables"], (query, variables)))


def livemeasurent_detailed_subscription() -> Dict[str, str]:
    """
    Query & variables to subscribe to timestamp, power, current per phase and voltage per phase
    :returns: dict {query: query_str, variables: query_variables}
    """
    query = """
    subscription ($homeid: ID!){
        liveMeasurement(homeId:$homeid){
            timestamp
            power
            currentL1
            currentL2
            currentL3
            voltagePhase1
            voltagePhase2
            voltagePhase3
            powerFactor
            maxPower
            minPower
            averagePower
            lastMeterConsumption
        }
    }
    """

    variables = {"homeid": os.getenv("HOME_ID")}

    return dict(zip(["query", "variables"], (query, variables)))


def subscribe(
    subscription_query: Callable, subscription_handler: Callable, **subscription_kwargs
):
    """
    subscribes to tibber pulse API for a specific query and handler for streaming data
    allows for passing additional subscription kwargs
    :param subscription_query: name of the subscription that returns the query and variables for the connection
    """
    return subscription_client.subscribe(
        headers={"Authorization": TIBBER_TOKEN},
        handle=subscription_handler,
        **subscription_query(),
        **subscription_kwargs
    )
