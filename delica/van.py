from logging import getLogger
from .exceptions import MissingRequiredException

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
