from __future__ import annotations
from delica.models.baseModel import DelicaBaseModel
from delica.endpoints import API_URL
from delica.exceptions import DelicaException


class People(DelicaBaseModel):
    def __init__(self, delica):
        """Initialize `.People` :class:

        Usage: delica.people
        """
        super().__init__(delica, _data=None)

    def find(self, person_id: int):
        if person_id:
            route = API_URL["find_people"]
        else:
            raise DelicaException

        return self._delica.get(route)
