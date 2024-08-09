from logging import getLogger
from typing import Any

import requests

from . import models
from .endpoints import API_URL
from .exceptions import MissingRequiredException, RequestException

logger = getLogger("delica")


class Van:
    """This is the VAN class that provides access to NGPVAN API

    Instances of this class help you accessing various parts
    of the VAN API. To instantiate a class:

    .. code-block:: python

    import delica

    van = delica.Van(
       api_application="APINAME",
       secret="SECRET"
    )
    """

    def __init__(self, application_name: str, api_key: str, version="v4"):
        """
        Initalize a :class: `.Van` instance.

        :param application_name: short string that identifies your application (e.g., acmeCrmProduct)
        :param api_key: string that identifies the specific context to which API requests should resolve. Specifically, it identifies an API user in an instance, database tab, and committee–the same information that is determined during the typical VAN login process

        Required parameters:
            - ``application_name``
            - ``api_key``
        """
        if not application_name or not api_key:
            raise MissingRequiredException(
                "Missing either application name or api key! You must provide either to create a van object"
            )

        self.application_name = application_name
        self.api_key = api_key
        self.version = version
        self.van_url = "https://api.securevan.com/v4"
        self._session = requests.Session()

        # Import all models
        self.people = models.People(self)

    def _request(self, *args: Any, **kwargs: Any):
        try:
            return self._session.request(*args, **kwargs)
        except Exception as e:  # noqa: BLE001
            raise RequestException(e, args, kwargs) from None

    def close_session(self):
        self._session.close()

    def _request_object(
        self,
        *,
        data: dict[str, str | Any] | None = None,
        json: dict[Any, Any] | list[Any] | None = None,
        method: str = "",
        params: str | dict[str, str] | None = None,
        path: str = ""
    ) -> Any:
        """Create a request object
        :param data: dict to send in the body of a request
        :param json: JSON object to send in the body of a request
        :param method: HTTP method
        :param params: Query params
        :param path: path
        """
        return self._request(
            data=data,
            json=json,
            method=method,
            params=params,
            path=path,
        )

    def get(self, path: str, *, params: str | None = None) -> Any:
        return self._request_object(method="GET", params=params, path=path)

    def post(self, path: str, *, data: Any | None = None, json: Any | None = None, params: str | None = None):
        if not json:
            data = data or {}

        return self._request_object(
            data=data,
            json=json,
            method="POST",
            params=params,
            path=path,
        )

    def _validate_keys(self):
        if self.api_key:
            route = API_URL["echo"]
        else:
            raise MissingRequiredException("Missing api_key!")

        return self.get(route)
