from __future__ import annotations
from typing import Any
from .exceptions import VanApiException


class DelicaBuilder:
    @classmethod
    def check_error(cls, data: list[Any] | Any):
        error = cls.error_parser(data)
        if error:
            raise error

    @classmethod
    def error_parser(cls, data: list[Any] | Any) -> VanApiException | None:
        if isinstance(data, list):
            return None

        errors = data.get("errors")
        if errors is None:
            return None

        return VanApiException

    def __init__(self, van, parsers: dict[str, Any] | None = None):
        """Initialize
        :param van: instance of :class: `.Van`
        """

        self.parsers = parsers if parsers else {}
        self._van = van

    def build(self, data):
        if data is None:
            return None

        if isinstance(data, list):
            return [self.build(item) for item in data]

        if "errors" in data:
            errors = data["errors"]
            if len(errors) > 0:
                raise VanApiException(errors)

        return data
