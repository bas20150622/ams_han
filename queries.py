# library for queries to Tibber pulse API
from python_graphql_client import GraphqlClient
from typing import Callable
from config import TIBBER_TOKEN

reqUrl = "https://api.tibber.com/v1-beta/gql"
headers = {"Authorization": "Bearer " + TIBBER_TOKEN}
client = GraphqlClient(endpoint=reqUrl, headers=headers)


def home_query(**kwargs):
    query = """
        query  {
            viewer {
                homes {
                    id
                }
            }
        }
    """
    variables = {}
    return dict(zip(["query", "variables"], (query, variables)))


def do_query(query_func: Callable, **kwargs):
    data = client.execute(**query_func(**kwargs))
    return data
