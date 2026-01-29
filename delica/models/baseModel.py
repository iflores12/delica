from __future__ import annotations

from typing import Any


class DelicaBaseModel:
    @classmethod
    def parse(cls, data, delica):
        return cls(delica, _data=data)

    def __init__(self, delica, _data: Any | None):
        self._delica = delica
        if _data:
            for attribute, value in _data.items():
                setattr(self, attribute, value)
