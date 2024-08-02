from __future__ import annotations
from .baseModel import DelicaBaseModel


class People(DelicaBaseModel):
    def __init__(self, delica):
        """Initialize `.People` :class:

        Usage: delica.people
        """
        super().__init__(delica, _data=None)

    def find(self, person_id: int):
        pass
