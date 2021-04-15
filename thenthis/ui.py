from datetime import datetime, timedelta
from functools import reduce
from typing import Optional, List
from pydantic import BaseModel
from whendo.sdk.client import Client
import whendo.core.util as util

class Pivot(BaseModel):
    name:str
    host:str
    port:Optional[int]=8000
    doc:Optional[str] = None

class Chain(BaseModel):
    """
    A Chain corresponds to a list of Pivots where the stop time of one pivot is equal
    to the start time of the next Pivot.
    """
    name:str
    pivots:List[Pivot]
    programs:List[str]
    durations:List[timedelta]

    def compute_stop(self, start: datetime):
        return start + reduce(lambda x, y: x + y, self.durations)

    def compute_times(self, start: datetime):
        last_start = start
        result = [last_start]
        for duration in self.durations:
            next_start = last_start + duration
            result.append(next_start)
            last_start = next_start
        return result

    def compute_pivot_times(self, start: datetime):
        """
        Returns a list of tuples of the form: (pivot, start, stop).
        """
        result = []
        times = self.compute_times(start=start)
        starts = times[:-1]
        stops = times[1:]
        datetime2s = [
            util.DateTime2(dt1=dt1, dt2=dt2) for dt1, dt2 in zip(starts, stops)
        ]
        result = list(zip(self.pivots, self.programs, datetime2s))
        return result

    def schedule_programs(self, start: datetime):
        pivot_times = self.compute_pivot_times(start=start)
        for pivot_time in pivot_times:
            pivot = pivot_time[0]
            program = pivot_time[1]
            datetime2 = pivot_time[2]
            Client(host=pivot.host, port=pivot.port).schedule_program(program_name=program, datetime2=datetime2)


class Flock(BaseModel):
    pivots:List[Pivot]
    chains:List[Chain]

    def get_pivot(self, name: str):
        try:
            return [pivot for pivot in self.pivots if pivot.name == name][0]
        except:
            return None

    def add_pivot(self, pivot: Pivot):
        self.pivots.append(pivot)

    def delete_pivot(self, pivot: Pivot):
        self.pivots.remove(pivot)

    def get_chain(self, name: str):
        try:
            return [chain for chain in self.chains if chain.name == name][0]
        except:
            return None

    def add_chain(self, chain: Chain):
        self.chains.append(chain)

    def delete_chain(self, chain: Chain):
        self.chains.remove(chain)

    def schedule_chain(self, name: str, start: datetime):
        chain = self.get_chain(name)
        for triple in chain.compute_pivot_times():
            triple[0].schedule_program(triple[1], triple[2])