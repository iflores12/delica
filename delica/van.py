import base64
import json
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
        self.van_url = f"https://api.securevan.com/{self.version}"
        self.credentials = f"{application_name}:{api_key}|{0}"
        self._session = requests.Session()
        # update session to include auth and content type
        self._session.headers.update(
            {
                "accept": "application/json",
                "content-type": "application/json",
                "authorization": f"Basic {base64.b64encode(self.credentials.encode()).decode()}",
            }
        )

        # Import all models
        self.people = models.People(self)

        self._validate_keys()

    def _request(self, *args: Any, **kwargs: Any):
        """

        Args:
            :
            :

        Raises:
            RequestException:

        Returns:

        """
        path = kwargs.pop("path", "")
        full_url = f"{self.van_url.rstrip('/')}/{path.lstrip('/')}"
        kwargs["url"] = full_url
        try:
            logger.debug(f"Request args: {args}, kwargs: {kwargs}")
            response = self._session.request(*args, **kwargs)
            response.raise_for_status()  # Raise an exception for HTTP errors

            return self._object_create(response)
        except requests.RequestException as e:
            logger.error(f"API Request failed: {e}")
            logger.error(f"Error Making Request to {full_url}")

            raise RequestException(og_exception=e, request_args=args, request_kwargs=kwargs) from e

    def close_session(self):
        self._session.close()

    def _request_object(
        self,
        *,
        data: dict[str, str | Any] | None = None,
        json: dict[Any, Any] | list[Any] | None = None,
        method: str = "",
        params: str | dict[str, str] | None = None,
        path: str = "",
    ) -> Any:
        """Create request object

        Args:
            data: data to send over or None
            json: if not sending data send json or None
            method: GET or POST
            params: params for request
            path: API path

        Raises:
            ValueError: If you don't specify a method then it raises a ValueError

        Returns: a request object based on the arguments you pass in

        """
        # Validate method is not empty
        if not method:
            raise ValueError("HTTP method must be specified")
        return self._request(
            data=data,
            json=json,
            method=method,
            params=params,
            path=path,
        )

    def _object_create(self, response):
        return json.loads(response.text)

    def get(self, path: str, *, params: str | None = None) -> Any:
        """Returns a request object from a GET request

        Args:
            path: Path to fetch
            params: Query params for request to VAN API

        Returns: A request object

        """
        return self._request_object(method="GET", params=params, path=path)

    def post(self, path: str, *, data: Any | None = None, json: Any | None = None, params: str | None = None):
        """

        Args:
            path: api route
            data: data to send or None
            json: json to send if not data or None
            params: params to send via request

        Raises:
            ValueError: raises error if you pass in both data and json

        Returns: A request object

        """
        if data is not None and json is not None:
            raise ValueError("Cannot specify both 'data' and 'json' parameters")

        payload = data or json or {}
        payload_type = "data" if data is not None else "json"

        return self._request_object(
            **{payload_type: payload},
            method="POST",
            params=params,
            path=path,
        )

    def _validate_keys(self):
        if self.api_key:
            route = API_URL["echo"]
        else:
            raise MissingRequiredException("Missing api_key!")

        return self.post(route, json={"message": "Hello"})
