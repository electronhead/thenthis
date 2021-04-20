from datetime import timedelta, datetime
from typing import List
from whendo.sdk.client import Client
import whendo.core.util as util
import thenthis.pi as pi_objs
from thenthis.ui import Pivot

pi3 = Pivot(
    name="pi3",
    host="192.168.0.46"
)
pi4 = Pivot(
        name="pi4",
        host="192.168.0.45"
        )

pivots = {
    pi3.name:pi3,
    pi4.name:pi4
}

actions = pi_objs.compute_actions()
schedulers = pi_objs.compute_schedulers()
programs = pi_objs.compute_programs()

def off(client:Client):
    client.execute_action("gpio_clear")

def reset(client: Client):
    try:
        client.stop_jobs()
    except:
        pass
    client.clear_jobs()
    client.clear_dispatcher()


def initialize_pivots():
    for pivot in pivots.values():
        client = Client(host=pivot.host, port=pivot.port)
        off(client)
        reset(client)
        [client.add_action(*action) for action in actions.items()]
        [client.add_scheduler(*scheduler) for scheduler in schedulers.items()]
        [client.add_program(*program) for program in programs.items()]
        client.run_jobs()

def schedule_programs(durations:List[timedelta] = [timedelta(seconds=30)]*len(pivots)):
    start=util.Now.dt()
    piv_dur = list(zip(pivots.values(), durations))
    for (pivot, duration) in piv_dur:
        stop = start + duration
        Client(host=pivot.host, port=pivot.port).schedule_program(
            program_name="pivot_program", 
            datetime2 = util.DateTime2(dt1=start, dt2=stop)
        )
        start = stop
