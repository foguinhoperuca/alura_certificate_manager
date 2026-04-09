from typing import Self

from value_object.workload import Workload


class Certificate:
    def __init__(self: Self, name: str, institution: str) -> None:
        self._name: str = name
        self._institution: str = institution
        self._classification: str = ''
        self._certificate_type: str = ''
        self._workload: Workload = Workload()
        self._filepath: str = ''
        self._start_date: str = ''
        self._end_date: str = ''
        self._emission_date: str = ''
