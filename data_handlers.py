"""
Module containing subscription data handlers
Data handlers process the api subsciption message data and include mechanics for interpolation of historical data
"""
from abc import ABC, abstractmethod


class AbstractSubscriptionData(ABC):
    """
    Abstract Base Class for subscription data feeds
    maintains internal cache of provided data and provides methods for
    processing mechanics of the data including print of the data

    Strips new data for None values that are considered invalid data
    """

    def __init__(self):
        self._cache = {}
        self._data_subkey = []

    def _get_query_data_key(self, data: dict):
        """Fetches the data_model key to fetch data from
        e.g. _get_query_data_key({'data':{'liveMeasurement':{'dp1':1, 'dp2':2}}}) returns ['data']['liveMeasurement']
        """
        for k, v in data.items():
            if isinstance(v, dict):
                self._data_subkey.append(k)
                return self._get_query_data_key(v)

    def _strip_null(self, data: dict) -> dict:
        """removes data keys with None value"""
        return {key: val for key, val in data.items() if val}

    def print(self, data: dict) -> dict:
        """print new data that has changed from cached data"""
        print(self._update(data))

    def _parse_data_from_model(self, data: dict) -> dict:
        """fetch the relevant data from datadict using the model keys"""
        if not self._data_subkey:
            # infer the data subkey dict
            self._get_query_data_key(data)

        res = data
        for subkey in self._data_subkey:
            res = res[subkey]
        return res

    @abstractmethod
    def _process(self, data: dict) -> dict:
        """
        the main processor for new data, determines what is passed back to print method
        """
        raise NotImplementedError

    def _update(self, data: dict) -> dict:
        data = self._parse_data_from_model(data)
        data = self._process(data)
        return data


class RawSubscriptionData(AbstractSubscriptionData):
    """
    straight data passthrough
    """

    def _process(self, data: dict) -> dict:
        return data


class CachedSubscriptionData(AbstractSubscriptionData):
    """
    prints new data in combination with old (unchanged) data
    """

    def _process(self, data: dict) -> dict:
        """
        provided new data to be compared against the cache, strips the null info, updates the cache,
        and returns the delta
        """
        filtered_data = self._strip_null(data)
        self._cache.update(filtered_data)
        return self._cache


class ValidSubscriptionData(AbstractSubscriptionData):
    """
    provides only valid (keys with values not null)
    - does not update cache
    """

    def _process(self, data: dict) -> dict:
        """
        returns only valid data - fully disregards cache
        """
        return self._strip_null(data)
