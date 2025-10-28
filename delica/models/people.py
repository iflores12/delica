from __future__ import annotations

from datetime import date

from delica.endpoints import API_URL
from delica.exceptions import DelicaException
from delica.models.baseModel import DelicaBaseModel


class People(DelicaBaseModel):
    def __init__(self, delica):
        """Initialize `.People` :class:

        Usage: delica.people
        """
        super().__init__(delica, _data=None)

    def find(self, *, person_query: dict | None = None):
        if person_query is None:
            raise DelicaException("Must provide a person query object to search")

        return self._delica.get(API_URL["find"], data=person_query)

    def find_person(self, person_id: int):
        if person_id:
            route = API_URL["find_people"]
        else:
            raise DelicaException("Person ID required")

        data = {"vanId": person_id}

        return self._delica.post(route, data=data)
